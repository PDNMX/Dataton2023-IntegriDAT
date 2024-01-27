
import pandas as pd
import numpy as np
from pprint import pprint

salida_paso1_preprocesar_s3 = "../salida_paso1_preprocesar_s3_generar_periodods_invalidez/"
salida_paso2_preprocesar_s6_pandas = "../salida_paso2_preprocesar_s6_pandas/"

s3_inhab = pd.read_pickle(salida_paso1_preprocesar_s3 + "inhabilitaciones.pkl")
#pprint(s3_inhab.columns)
#pprint(s3_inhab.shape)

s6_df = pd.read_hdf(salida_paso2_preprocesar_s6_pandas + "s6_hdf_dates.h5")
#pprint(s6_df.columns)
#pprint(s6_df.shape)

s3_inhab = s3_inhab.dropna(subset=["sancion_nombre", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"])
#pprint(s3_inhab.shape)
#pprint(s3_inhab.columns)


s3_inhab['inhabilitacion_fechaInicial'] = s3_inhab['inhabilitacion_fechaInicial'].apply(lambda x: pd.to_datetime(x, utc=True))
s3_inhab['inhabilitacion_fechaFinal'] = s3_inhab['inhabilitacion_fechaFinal'].apply(lambda x: pd.to_datetime(x, utc=True))

s3_inhab['inhabilitacion_fechaInicial'] = s3_inhab['inhabilitacion_fechaInicial'].dt.date
s3_inhab['inhabilitacion_fechaFinal'] = s3_inhab['inhabilitacion_fechaFinal'].dt.date


s6_df["parties_name"] = s6_df["parties_name"].str.lower().str.strip()
s6_df["parties_name"] = s6_df["parties_name"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

s6_df["parties_contactPoint_name"] = s6_df["parties_contactPoint_name"].str.lower().str.strip()
s6_df["parties_contactPoint_name"] = s6_df["parties_contactPoint_name"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


df1 = s3_inhab.merge(s6_df, left_on="sancion_nombre", right_on="parties_name", how = "inner", suffixes = ("s3", "s6") )
df2 = s3_inhab.merge(s6_df, left_on="sancion_nombre", right_on="parties_contactPoint_name", how = "inner", suffixes = ("s3", "s6") )
df = pd.concat([df1, df2])
pprint(df.shape)
pprint(df.columns)
pprint(df.head())
print("Informacion del dataframe")
pprint(df.info())
##df = df.drop_duplicates(keep="last")
##df = df.reset_index(drop = True)

##pprint(df.shape)
##pprint(df.columns)
##pprint(df.head())
#pprint("identificando duplicados")
#pprint(df.duplicated())

#df = df.drop_duplicates(keep="last")
#print(df.shape)
#print(df.columns)
#pprint(df.head())
""" 
df = df.dropna(subset=["inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal", "earliest_contractPeriod_startDate", "latest_contractPeriod_endDate"])

mask1 = df.earliest_contractPeriod_startDate.between(df.inhabilitacion_fechaInicial, df.inhabilitacion_fechaFinal)
mask2 = df.latest_contractPeriod_endDate.between(df.inhabilitacion_fechaInicial, df.inhabilitacion_fechaFinal)
final_mask = mask1 | mask2
df["contrato_durante_inhabilitacion"] = final_mask
df["contrato_durante_inhabilitacion"] = df["contrato_durante_inhabilitacion"].astype(int)
df_result = df[final_mask]
#df_result = df


df_result[["inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal", "earliest_contractPeriod_startDate", "latest_contractPeriod_endDate"]]

columnas_orden = ["sancion_nombre",'tipo_persona', 'sancion_tipoPersona', 'sancion_objetoSocial', 'inhabilitacion_fechaInicial',
                  'inhabilitacion_fechaFinal','earliest_contractPeriod_startDate', 'latest_contractPeriod_endDate', 'parties_name', "parties_contactPoint_name",
                  'ids3', 'expediente', '_id.$oid', 'ocid', 'ids6', 'contrato_durante_inhabilitacion']
df_result = df_result[columnas_orden]
df_result = df_result.reset_index(drop = True)

salida_paso3_resultado_cruzar_s3_s6 = "../salida_paso3_resultado_cruzar_s3_s6/"
df_result.to_excel(salida_paso3_resultado_cruzar_s3_s6 + "contrato_durante_inhabilitacion_IntegriDAT.xlsx", index=False)
"""