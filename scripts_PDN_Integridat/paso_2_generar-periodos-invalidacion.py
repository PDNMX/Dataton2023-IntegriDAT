#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse


# In[2]:


all_files_s3p = glob.glob(os.path.join("s3p" , "*/*.json"))
s3p_df_from_each_file = (pd.read_json(f) for f in all_files_s3p)
s3p_df = pd.concat(s3p_df_from_each_file, ignore_index=True)

all_files_s3s = glob.glob(os.path.join("s3s" , "*/*.json"))
s3s_df_from_each_file = (pd.read_json(f) for f in all_files_s3s)
s3s_df = pd.concat(s3s_df_from_each_file, ignore_index=True)


# # Procesar particulares sancionados

# In[3]:


def parse_date(x):
    try:
        return parse(x)
    except:
        return np.datetime64('NaT')


# In[4]:


sancionados = pd.json_normalize(s3p_df.particularSancionado)
inhabilitacion = pd.json_normalize(s3p_df.inhabilitacion)
inhabilitacion.fechaInicial =   inhabilitacion.fechaInicial.apply(parse_date)
inhabilitacion.fechaFinal = inhabilitacion.fechaFinal.apply(parse_date)


# In[5]:


s3p_df["sancion_nombre"] = sancionados.nombreRazonSocial
s3p_df["sancion_tipoPersona"] = sancionados.tipoPersona
s3p_df["sancion_objetoSocial"] = sancionados.objetoSocial
s3p_df["inhabilitacion_fechaInicial"] = inhabilitacion.fechaInicial
s3p_df["inhabilitacion_fechaFinal"] = inhabilitacion.fechaFinal
s3p_df["sancion_nombre"] = s3p_df["sancion_nombre"].str.lower()
s3p_df["sancion_nombre"] = s3p_df["sancion_nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[6]:


columnas = ["id", "expediente", "sancion_nombre", "sancion_tipoPersona", "sancion_objetoSocial", "inhabilitacion_fechaInicial","inhabilitacion_fechaFinal"]
s3p_df = s3p_df[columnas]
s3p_df["tipo_persona"] = "particular"
s3p_df[6:10]


# # Procesar servidores sancionados

# In[7]:


servidorPublicoSancionado = pd.json_normalize(s3s_df.servidorPublicoSancionado)
inhabilitacion_servidor = pd.json_normalize(s3s_df.inhabilitacion)


# In[8]:


s3s_df.columns


# In[9]:


servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]] = servidorPublicoSancionado[["nombres", "primerApellido", "segundoApellido" ]].fillna("")
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado.nombres + " " + servidorPublicoSancionado.primerApellido + " " + servidorPublicoSancionado.segundoApellido
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.lower().str.strip()
servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[10]:


servidorPublicoSancionado.isna().sum()


# In[11]:


servidorPublicoSancionado


# In[11]:


inhabilitacion_servidor.fechaInicial =  inhabilitacion_servidor.fechaInicial.apply(parse_date)
inhabilitacion_servidor.fechaFinal = inhabilitacion_servidor.fechaFinal.apply(parse_date)


# In[12]:


inhabilitacion_servidor.isna().sum()


# In[13]:


mask = (~inhabilitacion_servidor.fechaInicial.isna()) & (inhabilitacion_servidor.fechaFinal.isna())  
inhabilitacion_servidor[mask]


# In[14]:


s3s_df["sancion_nombre"] = servidorPublicoSancionado["nombre"]
s3s_df["inhabilitacion_fechaInicial"] = inhabilitacion_servidor.fechaInicial
s3s_df["inhabilitacion_fechaFinal"] = inhabilitacion_servidor.fechaFinal


# In[15]:


columnas = ["id", "expediente", "sancion_nombre", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"]
s3s_df = s3s_df[columnas]
s3s_df["tipo_persona"] = "servidor_publico"
s3s_df.head()


# # Combinar datasets

# In[16]:


df = pd.concat([s3p_df,s3s_df]).reset_index(drop = True)
df.head()


# In[17]:


df.to_pickle("inhabilitaciones.pkl")

