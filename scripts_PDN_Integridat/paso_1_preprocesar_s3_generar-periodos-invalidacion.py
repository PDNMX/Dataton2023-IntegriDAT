import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor

def parse_date(x):
    try:
        return parse(x)
    except:
        return np.datetime64('NaT')

def process_s3p_file(file_path):
    try:
        print(f"Leyendo archivo s3p: {file_path}")
        df = pd.read_json(file_path)
        sancionados = pd.json_normalize(df.particularSancionado)
        inhabilitacion = pd.json_normalize(df.inhabilitacion)
        inhabilitacion.fechaInicial = inhabilitacion.fechaInicial.apply(parse_date)
        inhabilitacion.fechaFinal = inhabilitacion.fechaFinal.apply(parse_date)

        df["sancion_nombre"] = sancionados.nombreRazonSocial
        df["sancion_tipoPersona"] = sancionados.tipoPersona
        df["sancion_objetoSocial"] = sancionados.objetoSocial
        df["inhabilitacion_fechaInicial"] = inhabilitacion.fechaInicial.dt.strftime('%Y-%m-%d')
        df["inhabilitacion_fechaFinal"] = inhabilitacion.fechaFinal.dt.strftime('%Y-%m-%d')
        df["sancion_nombre"] = df["sancion_nombre"].str.lower()
        df["sancion_nombre"] = df["sancion_nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        columnas = ["id", "expediente", "sancion_nombre", "sancion_tipoPersona", "sancion_objetoSocial", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"]
        df = df[columnas]
        df["tipo_persona"] = "particular"

        return df
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        return pd.DataFrame()

def process_s3s_file(file_path):
    try:
        print(f"Leyendo archivo s3s: {file_path}")
        df = pd.read_json(file_path)
        servidorPublicoSancionado = pd.json_normalize(df.servidorPublicoSancionado)
        inhabilitacion_servidor = pd.json_normalize(df.inhabilitacion)

        servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]] = servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]].fillna("")
        servidorPublicoSancionado["nombre"] = servidorPublicoSancionado.nombres + " " + servidorPublicoSancionado.primerApellido + " " + servidorPublicoSancionado.segundoApellido
        servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.lower().str.strip()
        servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        inhabilitacion_servidor.fechaInicial =  inhabilitacion_servidor.fechaInicial.apply(parse_date)
        inhabilitacion_servidor.fechaFinal = inhabilitacion_servidor.fechaFinal.apply(parse_date)

        mask = (~inhabilitacion_servidor.fechaInicial.isna()) & (inhabilitacion_servidor.fechaFinal.isna())  

        df["sancion_nombre"] = servidorPublicoSancionado["nombre"]
        df["inhabilitacion_fechaInicial"] = inhabilitacion_servidor.fechaInicial.dt.strftime('%Y-%m-%d')
        df["inhabilitacion_fechaFinal"] = inhabilitacion_servidor.fechaFinal.dt.strftime('%Y-%m-%d')

        columnas = ["id", "expediente", "sancion_nombre", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"]
        df = df[columnas]
        df["tipo_persona"] = "servidor_publico"

        return df
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        return pd.DataFrame()

# Obtener la lista de carpetas en "datos-pdn/s3p/" y "datos-pdn/s3s/"
all_folders_s3p = [f.path for f in os.scandir("datos-pdn/s3p/") if f.is_dir()]
all_folders_s3s = [f.path for f in os.scandir("datos-pdn/s3s/") if f.is_dir()]

# Inicializar listas para almacenar los DataFrames de cada carpeta
s3p_dfs = []
s3s_dfs = []

# Utilizar ThreadPoolExecutor para procesar las carpetas en paralelo
with ThreadPoolExecutor() as executor:
    # Procesar archivos s3p
    for folder_path in all_folders_s3p:
        all_files_s3p = glob.glob(os.path.join(folder_path, "*.json"))
        s3p_dfs.extend(list(executor.map(process_s3p_file, all_files_s3p)))

    # Procesar archivos s3s
    for folder_path in all_folders_s3s:
        all_files_s3s = glob.glob(os.path.join(folder_path, "*.json"))
        s3s_dfs.extend(list(executor.map(process_s3s_file, all_files_s3s)))

# Concatenar todos los DataFrames de s3p y s3s
s3p_df = pd.concat(s3p_dfs, ignore_index=True)
s3s_df = pd.concat(s3s_dfs, ignore_index=True)

# Combinar ambos DataFrames
combined_df = pd.concat([s3p_df, s3s_df], ignore_index=True)

# Guardar el DataFrame combinado en un archivo JSON
combined_df.to_json("inhabilitaciones.json", orient="records")
