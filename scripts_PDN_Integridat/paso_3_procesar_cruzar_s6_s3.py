#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import numpy as np


# In[20]:


s3_inhab = pd.read_pickle("inhabilitaciones.pkl")
s6_df = pd.read_hdf("s6_hdf_dates.h5")


# In[21]:


s3_inhab = s3_inhab.dropna(subset=["sancion_nombre", "inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal"])

s3_inhab['inhabilitacion_fechaInicial'] = s3_inhab['inhabilitacion_fechaInicial'].apply(lambda x: pd.to_datetime(x, utc=True))
s3_inhab['inhabilitacion_fechaFinal'] = s3_inhab['inhabilitacion_fechaFinal'].apply(lambda x: pd.to_datetime(x, utc=True))

s3_inhab['inhabilitacion_fechaInicial'] = s3_inhab['inhabilitacion_fechaInicial'].dt.date
s3_inhab['inhabilitacion_fechaFinal'] = s3_inhab['inhabilitacion_fechaFinal'].dt.date


# In[22]:


s6_df["parties_name"] = s6_df["parties_name"].str.lower().str.strip()
s6_df["parties_name"] = s6_df["parties_name"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

s6_df["parties_contactPoint_name"] = s6_df["parties_contactPoint_name"].str.lower().str.strip()
s6_df["parties_contactPoint_name"] = s6_df["parties_contactPoint_name"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[23]:


s3_inhab.head()


# In[24]:


s6_df.head()


# In[25]:


df1 = s3_inhab.merge(s6_df, left_on="sancion_nombre", right_on="parties_name", how = "inner", suffixes = ("s3", "s6") )
df2 = s3_inhab.merge(s6_df, left_on="sancion_nombre", right_on="parties_contactPoint_name", how = "inner", suffixes = ("s3", "s6") )
df = pd.concat([df1, df2])
df = df.drop_duplicates()


# In[26]:


df.shape


# In[27]:


df = df.dropna(subset=["inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal", "earliest_contractPeriod_startDate", "latest_contractPeriod_endDate"])
df.shape


# In[28]:


df.head(3)


# In[29]:


mask1 = df.earliest_contractPeriod_startDate.between(df.inhabilitacion_fechaInicial, df.inhabilitacion_fechaFinal)
mask2 = df.latest_contractPeriod_endDate.between(df.inhabilitacion_fechaInicial, df.inhabilitacion_fechaFinal)
final_mask = mask1 | mask2
df["contrato_durante_inhabilitacion"] = final_mask
df["contrato_durante_inhabilitacion"] = df["contrato_durante_inhabilitacion"].astype(int)
df_result = df[final_mask]
#df_result = df


# In[30]:


df_result[["inhabilitacion_fechaInicial", "inhabilitacion_fechaFinal", "earliest_contractPeriod_startDate", "latest_contractPeriod_endDate"]]


# In[31]:


df_result.head()


# In[32]:


df_result.columns


# In[33]:


columnas_orden = ["sancion_nombre",'tipo_persona', 'sancion_tipoPersona', 'sancion_objetoSocial', 'inhabilitacion_fechaInicial',
                  'inhabilitacion_fechaFinal','earliest_contractPeriod_startDate', 'latest_contractPeriod_endDate', 'parties_name', "parties_contactPoint_name",
                  'ids3', 'expediente', '_id.$oid', 'ocid', 'ids6', 'contrato_durante_inhabilitacion']
df_result = df_result[columnas_orden]
df_result = df_result.reset_index(drop = True)


# In[34]:


df_result.head()


# In[35]:


df_result.to_excel("contrato_durante_inhabilitacion_IntegriDAT.xlsx", index=False)

