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
import gc


# In[2]:


declaracion = pd.read_pickle("s1_declaracion.pkl")


# In[3]:


def parse_date(x):
    try:
        return parse(x)
    except:
        return np.datetime64('NaT')


# In[4]:


declaracion.columns


# In[21]:


declaracion["situacionPatrimonial.datosGenerales.nombre"] = declaracion["situacionPatrimonial.datosGenerales.nombre"].fillna("")
declaracion["situacionPatrimonial.datosGenerales.primerApellido"] = declaracion["situacionPatrimonial.datosGenerales.primerApellido"].fillna("")
declaracion["situacionPatrimonial.datosGenerales.segundoApellido"] = declaracion["situacionPatrimonial.datosGenerales.segundoApellido"].fillna("")

declaracion["nombre_declaracion"] = declaracion["situacionPatrimonial.datosGenerales.nombre"] + " " \
+ declaracion["situacionPatrimonial.datosGenerales.primerApellido"] + " " \
+ declaracion["situacionPatrimonial.datosGenerales.segundoApellido"]

declaracion["nombre_declaracion"] = declaracion["nombre_declaracion"].str.lower().str.strip()
declaracion["nombre_declaracion"] = declaracion["nombre_declaracion"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

declaracion ["fechaTomaPosesion"] =  declaracion["situacionPatrimonial.datosEmpleoCargoComision.fechaTomaPosesion"].apply(parse_date)

columnas = ["nombre_declaracion" , "fechaTomaPosesion"]
declaracion_target = declaracion[columnas]


# In[22]:


declaracion_target


# In[29]:


declaracion_target.to_hdf("s1_fecha_toma_posesion.h5", key = "df")


# In[ ]:




