import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse

def parse_date(x):
    try:
        return parse(x)
    except:
        return np.datetime64('NaT')
    
all_files_s3p = glob.glob(os.path.join("../s3p" , "*/*.json"))
s3p_df_from_each_file = (pd.read_json(f) for f in all_files_s3p)
s3p_df = pd.concat(s3p_df_from_each_file, ignore_index=True)

all_files_s3s = glob.glob(os.path.join("../s3s" , "*/*.json"))
s3s_df_from_each_file = (pd.read_json(f) for f in all_files_s3s)
s3s_df = pd.concat(s3s_df_from_each_file, ignore_index=True)

sancionados = pd.json_normalize(s3p_df.particularSancionado)
inhabilitacion = pd.json_normalize(s3p_df.inhabilitacion)
inhabilitacion.fechaInicial =   inhabilitacion.fechaInicial.apply(parse_date)
inhabilitacion.fechaFinal = inhabilitacion.fechaFinal.apply(parse_date)

s3p_df["sancion_nombre"] = sancionados.nombreRazonSocial
s3p_df["sancion_tipoPersona"] = sancionados.tipoPersona
s3p_df["sancion_objetoSocial"] = sancionados.objetoSocial
s3p_df["inhabilitacion_fechaInicial"] = inhabilitacion.fechaInicial
s3p_df["inhabilitacion_fechaFinal"] = inhabilitacion.fechaFinal
s3p_df["sancion_nombre"] = s3p_df["sancion_nombre"].str.lower()
s3p_df["sancion_nombre"] = s3p_df["sancion_nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

columnas = ["id", "expediente", "sancion_nombre", "sancion_tipoPersona", "sancion_objetoSocial", "inhabilitacion_fechaInicial","inhabilitacion_fechaFinal"]
s3p_df = s3p_df[columnas]
s3p_df["tipo_persona"] = "particular"
#s3p_df[6:10]

servidorPublicoSancionado = pd.json_normalize(s3s_df.servidorPublicoSancionado)
inhabilitacion_servidor = pd.json_normalize(s3s_df.inhabilitacion)

servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]] = servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]].fillna("")
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado.nombres + " " + servidorPublicoSancionado.primerApellido + " " + servidorPublicoSancionado.segundoApellido
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.lower().str.strip()
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

inhabilitacion_servidor.fechaInicial =  inhabilitacion_servidor.fechaInicial.apply(parse_date)
inhabilitacion_servidor.fechaFinal = inhabilitacion_servidor.fechaFinal.apply(parse_date)

mask = (~inhabilitacion_servidor.fechaInicial.isna()) & (inhabilitacion_servidor.fechaFinal.isna())  
#inhabilitacion_servidor[mask]

s3s_df["sancion_nombre"] = servidorPublicoSancionado["nombre"]
s3s_df["inhabilitacion_fechaInicial"] = inhabilitacion_servidor.fechaInicial
s3s_df["inhabilitacion_fechaFinal"] = inhabilitacion_servidor.fechaFinal

columnas = ["id", "expediente", "sancion_nombre", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"]
#s3s_df = s3s_df[columnas]
s3s_df["tipo_persona"] = "servidor_publico"
#s3s_df.head()

df = pd.concat([s3p_df,s3s_df]).reset_index(drop = True)

salida_paso1_s3 = "../salida_paso1_preprocesar_s3_generar_periodods_invalidez/"
df.to_pickle(salida_paso1_s3 + "inhabilitaciones.pkl")