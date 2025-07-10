import pandas as pd
import os
import glob
import datetime
from dateutil.parser import parse
import gc
from tqdm import tqdm
tqdm.pandas()
from itertools import islice
from pprint import pprint

diccionario_roles = {
    "buyer": "Comprador",
    "procuringEntity": "Entidad contratante",
    "supplier": "Proveedor",
    "tenderer": "Licitante",
    "funder": "Financiador",
    "payer": "Pagador",
    "payee": "Beneficiario",
    "reviewBody": "Órgano revisor",
    "interestedParty": "Parte interesada"
    }

def parse_date(x):
    try:
        return parse(x)
    except:
        return None

def find_dates_no_processing(awards):
    start_dates = []
    end_dates = []
    if type(awards) is list:
        for award in awards:
            if type(award) is dict:
                start_date = award.get("contractPeriod", {}).get("startDate")
                start_dates.append(start_date)
                end_date = award.get("contractPeriod",{}).get("endDate")
                end_dates.append(end_date)
        return start_dates, end_dates
    else:
        return [], []

def extract_parties_names(parties):
    if type(parties) is dict:
        name = parties.get("name")
        contact = parties.get("contactPoint", {}).get("name")
        return name, contact
    else:
        return "", ""

def get_address_string(address):
    if address is not None:
        return ",".join([
            address.get("countryName", ""),
            address.get("locality", ""),
            address.get("postalCode", ""),
            address.get("region", ""),
            address.get("streetAddress", "")
        ])
    else:
        return ""

def datos_procuriEntity(df):
    df['procuring_entity'] = df['parties'].apply(lambda x: [party['name'] for party in x if 'procuringEntity' in party.get('roles', [])][0] if any('procuringEntity' in party.get('roles', []) for party in x) else None)
    df['procuring_entity_region'] = df['parties'].apply(lambda x: [party['address'].get("region") for party in x if 'procuringEntity' in party.get('roles', [])][0] if any('procuringEntity' in party.get('roles', []) for party in x) else None)
    df['procuring_entity_country'] = df['parties'].apply(lambda x: [party['address'].get("country") for party in x if 'procuringEntity' in party.get('roles', [])][0] if any('procuringEntity' in party.get('roles', []) for party in x) else None)
    df['procuring_entity_locality'] = df['parties'].apply(lambda x: [party['address'].get("locality") for party in x if 'procuringEntity' in party.get('roles', [])][0] if any('procuringEntity' in party.get('roles', []) for party in x) else None)
    df['procuring_entity_streetAddress'] = df['parties'].apply(lambda x: [party['address'].get("streetAddress") for party in x if 'procuringEntity' in party.get('roles', [])][0] if any('procuringEntity' in party.get('roles', []) for party in x) else None)
    return df

def extraer_S6(df):
    df = datos_procuriEntity(df)
    keep_cols = ['_id', "ocid", "id", "parties", "awards", "procuring_entity", "procuring_entity_region", "procuring_entity_country", "procuring_entity_locality", "procuring_entity_streetAddress"]
    df = df[keep_cols]
    res = df.awards.map(find_dates_no_processing)
    df["contractPeriod_startDate"], df["contractPeriod_endDate"] = zip(*res)
    df = df.drop(columns=["awards"])
    df = df.explode("parties")
    res_contact = df.parties.map(extract_parties_names)
    df["parties_name"], df["parties_contactPoint_name"] = zip(*res_contact)
    df["entidadFederativa"] = df.parties.map(lambda x: x.get("address", {}).get("region"))
    df["parties_address"] = df.parties.map(get_address_string)
    df["parties_roles"] = df.parties.map(lambda x: x.get("roles", []))
    df = df.drop(columns=["parties"])
    df = df.reset_index(drop = True)
    return df

def procesar_estructura_anidada(df_raw):
    """
    Procesa la nueva estructura anidada donde los datos están en 'record'
    """
    records = []
    
    for index, row in df_raw.iterrows():
        # Extraer datos del record
        record_data = row.get('record', {})
        
        # Agregar información del nivel superior
        record_data['metadata'] = row.get('metadata', {})
        record_data['_id_original'] = row.get('_id', {})
        
        records.append(record_data)
    
    # Crear DataFrame con los records procesados
    df_processed = pd.DataFrame(records)
    
    return df_processed

def convert_files_parquet_h5(df, directorio_salida, nombre_archivo, i):
    try:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_parquet(directorio_salida+str(nombre_archivo)+"_parquet_" + str(i) + ".parquet")
    except Exception as e:
        print(f"Error al guardar parquet: {e}")
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_hdf(directorio_salida +str(nombre_archivo) + "_s6_hdf_" + str(i) + ".h5", key = "s6_df")

def convert_files_h5_parquet(df, directorio_salida, nombre_archivo, i):
    try:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_hdf(directorio_salida +str(nombre_archivo) + "_s6_hdf_" + str(i) + ".h5", key = "s6_df")
    except Exception as e:
        print(f"Error al guardar HDF5: {e}")
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_parquet(directorio_salida+str(nombre_archivo)+"_parquet_" + str(i) + ".parquet")

def procesar_archivo(ruta_archivo, nombre_archivo, directorio_salida, i):
    """
    Procesa un archivo individual con la nueva estructura
    """
    try:
        # Leer el archivo JSON
        df_raw = pd.read_json(ruta_archivo)
        print(f"Archivo leído: {nombre_archivo}, Shape original: {df_raw.shape}")
        
        # Procesar la estructura anidada
        df_processed = procesar_estructura_anidada(df_raw)
        print(f"Después de procesar estructura: {df_processed.shape}")
        
        # Verificar que tenemos las columnas necesarias
        columnas_necesarias = ['_id', 'ocid', 'id', 'parties', 'awards']
        columnas_faltantes = [col for col in columnas_necesarias if col not in df_processed.columns]
        
        if columnas_faltantes:
            print(f"Advertencia: Columnas faltantes en {nombre_archivo}: {columnas_faltantes}")
            # Agregar columnas faltantes con valores vacíos
            for col in columnas_faltantes:
                df_processed[col] = None
        
        # Aplicar el procesamiento S6
        df_s6 = extraer_S6(df_processed)
        print(f"Después de extraer S6: {df_s6.shape}")
        
        # Guardar el archivo procesado
        convert_files_parquet_h5(df_s6, directorio_salida, nombre_archivo, i)
        
        return True
        
    except Exception as e:
        print(f"Error procesando archivo {nombre_archivo}: {e}")
        return False

### Leer por carpeta o directorio y nombre de archivo o json
### Se itera sobre el directorio
ruta_bulk_s6_nombres = '/home/phoenix/sesna/desarrollo/otros/bulk_datos_sergio_09_07_2025/s6/output'
contenido_ruta_bulk_s6 = os.listdir(ruta_bulk_s6_nombres)
salida_preprocesamiento_s6 = '/home/phoenix/sesna/desarrollo/otros/bulk_datos_sergio_09_07_2025/cruces_integridat/paso_1_preprocesar_s6_pandas/'

print("Ruta de entrada:", ruta_bulk_s6_nombres)
print("Ruta de salida:", salida_preprocesamiento_s6)

# Crear directorio de salida si no existe
os.makedirs(salida_preprocesamiento_s6, exist_ok=True)

archivos_procesados = 0
archivos_con_error = 0

for i in range(len(contenido_ruta_bulk_s6)):
    elemento = contenido_ruta_bulk_s6[i]
    ruta_elemento = os.path.join(ruta_bulk_s6_nombres, elemento)
    
    if os.path.isfile(ruta_elemento):
        print(f"\nProcesando archivo: {elemento}")
        if procesar_archivo(ruta_elemento, elemento, salida_preprocesamiento_s6, i):
            archivos_procesados += 1
        else:
            archivos_con_error += 1
    
    elif os.path.isdir(ruta_elemento):
        print(f"\nProcesando directorio: {elemento}")
        contenido_subdirectorio = os.listdir(ruta_elemento)
        
        for j, archivo_sub in enumerate(contenido_subdirectorio):
            ruta_archivo_sub = os.path.join(ruta_elemento, archivo_sub)
            
            if os.path.isfile(ruta_archivo_sub):
                print(f"  Procesando archivo en subdirectorio: {archivo_sub}")
                if procesar_archivo(ruta_archivo_sub, archivo_sub, salida_preprocesamiento_s6, j):
                    archivos_procesados += 1
                else:
                    archivos_con_error += 1

print(f"\n=== RESUMEN ===")
print(f"Archivos procesados correctamente: {archivos_procesados}")
print(f"Archivos con error: {archivos_con_error}")
print("Obtención de las nuevas columnas del S6")
print("Fin del preproceso de los archivos del S6")