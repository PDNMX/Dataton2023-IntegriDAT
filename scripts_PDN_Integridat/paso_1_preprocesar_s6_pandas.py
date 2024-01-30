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


def extraer_S6(df):
    keep_cols = ['_id', "ocid", "id", "parties", "awards" ]
    df = df[keep_cols]
    res = df.awards.map(find_dates_no_processing)
    df["contractPeriod_startDate"], df["contractPeriod_endDate"] = zip(*res)
    #df.loc[:, "contractPeriod_startDate"], df.loc[:, "contractPeriod_endDate"] = zip(*res)
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



def convert_files_parquet_h5(df, directorio_salida, nombre_archivo, i):
    try:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_parquet(directorio_salida+str(nombre_archivo)+"_parquet_" + str(i) + ".parquet")
    except Exception as e:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_hdf(directorio_salida +str(nombre_archivo) + "_s6_hdf_" + str(i) + ".h5", key = "s6_df")

def convert_files_h5_parquet(df, directorio_salida, nombre_archivo, i):
    try:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_hdf(directorio_salida +str(nombre_archivo) + "_s6_hdf_" + str(i) + ".h5", key = "s6_df")
    except Exception as e:
        nombre_archivo = nombre_archivo.split(".")[0]
        df.to_parquet(directorio_salida+str(nombre_archivo)+"_parquet_" + str(i) + ".parquet")


### Leer por carpeta o directorio y nombre de archivo o json
### Se iterqa sobre el directorio
ruta_bulk_s6_nombres = '../bulk-s6'
contenido_ruta_bulk_s6 = os.listdir(ruta_bulk_s6_nombres)
salida_preprocesamiento_s6 = '../salida_paso1_s6_pandas/'
pprint(ruta_bulk_s6_nombres)

for i in range(len(contenido_ruta_bulk_s6)):
    #print("Iteracion: ", i)
    ##solo para listar lo que se itera
    ##print("Archivo: ", contenido_ruta_bulk_s6[i])
    if os.path.isfile(ruta_bulk_s6_nombres +'/'+contenido_ruta_bulk_s6[i]) == True:
        #print("Es un archivo")
        nombre_archivo = contenido_ruta_bulk_s6[i]
        #print("Archivo: ", nombre_archivo)
        ruta_archivo = ruta_bulk_s6_nombres +'/'+contenido_ruta_bulk_s6[i]
        #rint("Ruta archivo: ", ruta_archivo)
        df = pd.read_json(ruta_bulk_s6_nombres +'/'+contenido_ruta_bulk_s6[i])
        #pprint(df.shape)
        df = extraer_S6(df)
        convert_files_parquet_h5(df, salida_preprocesamiento_s6, nombre_archivo, i)
        ##convert_files_h5_parquet(df, salida_preprocesamiento_s6, nombre_archivo, i)

    if os.path.isdir(ruta_bulk_s6_nombres +'/'+contenido_ruta_bulk_s6[i]) == True:
        pass
        #print("Es un directorio")
        ## listar el contenido del subdirectorio
        contenido_subdirectorio = os.listdir(ruta_bulk_s6_nombres +'/'+contenido_ruta_bulk_s6[i])
        x=0
        #print("Contenido subdirectorio: ", contenido_subdirectorio)
        for j in range(len(contenido_subdirectorio)):
            #print("Iteracion subdirectorio: ", j)
            #print("Archivo: ", contenido_subdirectorio[j])
            nombre_archivo_subdirectorio = ruta_bulk_s6_nombres +'/'+ contenido_ruta_bulk_s6[i] + '/'+ contenido_subdirectorio[j]
            df = pd.read_json(nombre_archivo_subdirectorio)
            #pprint(df.shape)
            df = extraer_S6(df)
            convert_files_parquet_h5(df, salida_preprocesamiento_s6, contenido_subdirectorio[j], j)
            ##convert_files_h5_parquet(df, salida_preprocesamiento_s6, contenido_subdirectorio[j], j)
            #pprint(contenido_subdirectorio[j])
            #df = pd.read_json(contenido_subdirectorio[j], lines=True)
            #print("Tamaño del dataframe: ", df.shape)
print("Obtencion de las nuevas columnas del S6")
pprint("Fin del preproceso de los archivos del S6")