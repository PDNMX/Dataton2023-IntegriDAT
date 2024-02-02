import pandas as pd
import numpy as np
from dateutil.parser import parse
from tqdm import tqdm
tqdm.pandas()
import os
from pprint import pprint 
import pyarrow as pa

def parse_date(x):
    try:
        return parse(x)
    except:
        return None
    
def find_earliest_date(dates):
    try:
        if len(dates) > 0:
            dates = [parse_date(date) for date in dates]
            dates = [x for x in dates if x is not None]
            if len(dates) > 0:
                earliest = min(dates)
            else:
                earliest = None
        else:
            earliest = None
        return earliest
    except:
        return None
    
            
def find_latest_date(dates):
    try:
        if len(dates) > 0:
            dates = [parse_date(date) for date in dates]
            dates = [x for x in dates if x is not None]
            if len(dates) > 0:
                latest = max(dates)
            else:
                latest = None
        else:
            latest = None
        return latest
    except:
        return None
        

### Leer ztodos los archivos del S6 en formato parquet

ruta_salida_paso1_s6_pandas = '../salida_paso1_s6_pandas/'
contenido_salida_paso1_s6_pandas = os.listdir(ruta_salida_paso1_s6_pandas)
#pprint(contenido_salida_paso1_s6_pandas)
df_list = []
salida_paso2_preprocesar_s6_pandas = '../salida_paso2_preprocesar_s6_pandas/'

for archivo in contenido_salida_paso1_s6_pandas:
    df = pd.read_parquet(ruta_salida_paso1_s6_pandas + archivo)
    df["earliest_contractPeriod_startDate"] = df.contractPeriod_startDate.progress_apply(find_earliest_date)
    df["latest_contractPeriod_endDate"] = df.contractPeriod_endDate.progress_apply(find_latest_date)
    #pprint(df.head())
    df_list.append(df)

df_s6 = pd.concat(df_list)
pprint(df_s6.head())
pprint(df_s6.shape)
pprint(df_s6.columns)
df_s6.to_hdf(salida_paso2_preprocesar_s6_pandas + "s6_hdf_dates.h5", key = "s6_df")
print("paso_2_preprocesar_fechas_s6 y generacion de archivo s6_hdf_dates.h5 Terminado")