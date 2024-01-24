import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse
import gc
from tqdm import tqdm
tqdm.pandas()
from itertools import islice
#import polars as pl
from pprint import pprint
from time import sleep

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

def convert_files_parquet_h5(df, directorio_salida, nombre_archivo, i):
    try:
        df.to_parquet(directorio_salida+str(nombre_archivo)+"_parquet_" + str(i) + ".parquet")
    except Exception as e:
        df.to_hdf(directorio_salida +str(nombre_archivo) + "_s6_hdf_" + str(i) + ".h5", key = "s6_df")


def extraer_S6(df):
    keep_cols = ['_id', "ocid", "id", "parties", "awards"]
    df = df[keep_cols]
    #pprint(df.shape)
    #pprint(df.columns)
    res = df.awards.progress_apply(find_dates_no_processing)
    #pprint(res)
    df["contractPeriod_startDate"], df["contractPeriod_endDate"] = zip(*res)
    df = df.drop(columns=["awards"])
    #pprint(df.columns)
    #pprint(s6_df.head())
    df = df.explode("parties")
    res_contact = df.parties.map(extract_parties_names)
    #pprint(res_contact)
    df["parties_name"], df["parties_contactPoint_name"] = zip(*res_contact)
    df = df.drop(columns=["parties"])
    df = df.reset_index(drop = True)
    #pprint(df)
    return df


### Leer por carpeta o directorio y nombre de archivo o json
### Se iterqa sobre el directorio
ruta_bulk_s6_todo = '../bulk-s6'
ruta_bulk_s6 = os.listdir(ruta_bulk_s6_todo)
pprint(ruta_bulk_s6)
#print(ruta_bulk_s6[0])
salida = "salidas_remake_s6_pandas/"

i = 0
for i in range(len(ruta_bulk_s6)):
    print(ruta_bulk_s6[i])
    #df = pd.read_json('bulk-s6/'+ruta_bulk_s6[i], lines=True)
    if os.path.isdir('bulk-s6/'+ruta_bulk_s6[i]) == True:
        #print("es un directorio")
        #print(ruta_bulk_s6[i]) 
        nombre_directorio = 'bulk-s6/'+ruta_bulk_s6[i]+'/*.json'
        #print("cadena")
        #print(nombre_directorio)
        lista_directorio = glob.glob(nombre_directorio)
        #pprint(lista_directorios)
        x=0
        for j in range(len(lista_directorio)):
            df = pd.read_json(lista_directorio[j])
            print("archivo desde directorio")
            print(lista_directorio[j])
            #pprint(lista_directorio[j])
            #print(df.shape)
            nombre_archivo = lista_directorio[j].split(".")[0]
            print(nombre_archivo)
            df = extraer_S6(df)
            convert_files_parquet_h5(df, salida, nombre_archivo, x)
            x+=1
    if os.path.isfile('bulk-s6/'+ruta_bulk_s6[i]) == True:
        #print("es un archivo")
        nombre_archivo = 'bulk-s6/' + ruta_bulk_s6[i]
        nombre_archivo.split(".")[0]
        #pprint(nombre_archivo)
        ##df = pd.read_json(nombre_archivo)
        #pprint("nombre archivo desde raiz")
        #pprint(df.shape)
        #pprint(df.columns)
        #convert_files_parquet(df, salida, nombre_archivo, i)
    i+=1
    print("iteracion" + str(i))
    