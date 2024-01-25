import numpy as np
import pandas as pd
import pathlib

def parse_date(x):
    try:
        return parse(x)
    except:
        return np.datetime64('NaT')


all_files_s3p = pathlib.Path("../s3p").glob("**/*.json")
all_files_s3s = pathlib.Path("../s3s").glob("**/*.json")

s3p_df = pd.concat(list(map(pd.read_json, all_files_s3p)), ignore_index=True)
s3s_df = pd.concat(list(map(pd.read_json, all_files_s3s)), ignore_index=True)

s3p_df["sancion_nombre"] = pd.json_normalize(s3p_df.particularSancionado)["nombreRazonSocial"]
s3p_df["sancion_tipoPersona"] = pd.json_normalize(s3p_df.particularSancionado)["tipoPersona"]
s3p_df["sancion_objetoSocial"] = pd.json_normalize(s3p_df.particularSancionado)["objetoSocial"]
s3p_df["inhabilitacion_fechaInicial"] = pd.json_normalize(s3p_df.inhabilitacion)["fechaInicial"].apply(parse_date)
s3p_df["inhabilitacion_fechaFinal"] = pd.json_normalize(s3p_df.inhabilitacion)["fechaFinal"].apply(parse_date)

s3s_df["sancion_nombre"] = pd.json_normalize(s3s_df.servidorPublicoSancionado)["nombre"]
s3s_df["inhabilitacion_fechaInicial"] = pd.json_normalize(s3s_df.inhabilitacion)["fechaInicial"].apply(parse_date)
s3s_df["inhabilitacion_fechaFinal"] = pd.json_normalize(s3s_df.inhabilitacion)["fechaFinal"].apply(parse_date)

s3s_df = s3s_df.loc[~s3s_df.inhabilitacion_fechaInicial.isna()]

df = pd.concat([s3p_df, s3s_df], ignore_index=True)
df["tipo_persona"] = df.apply(lambda x: "particular" if x.sancion_tipoPersona == "particular" else "servidor_publico", axis=1)

df.to_pickle("inhabilitaciones.pkl")
