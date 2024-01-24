#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import numpy as np
from dateutil.parser import parse


# In[90]:


s3_inhab = pd.read_pickle("inhabilitaciones.pkl")
s1_posesion = pd.read_hdf("s1_fecha_toma_posesion.h5")


# In[91]:


s1_posesion.head()


# In[92]:


s3_inhab.head()


# In[93]:


df = s1_posesion.merge(s3_inhab, left_on="nombre_declaracion", right_on="sancion_nombre", how = "inner", suffixes = ("s1", "s3") )


# In[94]:


df = df.drop_duplicates()


# In[95]:


df = df.dropna(subset=["nombre_declaracion","fechaTomaPosesion", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"])


# In[96]:


df['fechaTomaPosesion'] = df['fechaTomaPosesion'].apply(lambda x: pd.to_datetime(x, utc=True))
df['inhabilitacion_fechaInicial'] = df['inhabilitacion_fechaInicial'].apply(lambda x: pd.to_datetime(x, utc=True))
df['inhabilitacion_fechaFinal'] = df['inhabilitacion_fechaFinal'].apply(lambda x: pd.to_datetime(x, utc=True))

df['fechaTomaPosesion'] = df['fechaTomaPosesion'].dt.date
df['inhabilitacion_fechaInicial'] = df['inhabilitacion_fechaInicial'].dt.date
df['inhabilitacion_fechaFinal'] = df['inhabilitacion_fechaFinal'].dt.date

df["posesion_durante_inhabilitacion"] = df.fechaTomaPosesion.between(df.inhabilitacion_fechaInicial, df.inhabilitacion_fechaFinal)


# In[97]:


df[["nombre_declaracion","fechaTomaPosesion", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal", "posesion_durante_inhabilitacion"]]


# In[98]:


df.posesion_durante_inhabilitacion.sum()


# In[99]:


mask = df.posesion_durante_inhabilitacion
df["posesion_durante_inhabilitacion"] = df["posesion_durante_inhabilitacion"].astype(int)


# In[100]:


resultado = df[mask]


# In[101]:


len(resultado.nombre_declaracion.unique())


# In[102]:


resultado = resultado.sort_values(by = "nombre_declaracion")
resultado = resultado.reset_index(drop=True)
resultado = resultado.drop(columns=["sancion_tipoPersona", "sancion_objetoSocial"])


# In[103]:


resultado.tipo_persona.value_counts()


# In[104]:


columnas_orden = ['nombre_declaracion', 'id', 'expediente', 'fechaTomaPosesion', 
       'inhabilitacion_fechaInicial', 'inhabilitacion_fechaFinal', 'posesion_durante_inhabilitacion']
resultado = resultado[columnas_orden]


# In[105]:


resultado


# In[106]:


resultado.to_excel("posesion_durante_inhabilitacion_IntegriDAT.xlsx", index=False)

