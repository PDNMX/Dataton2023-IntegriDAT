#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[ ]:


import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse
import gc


# In[2]:


all_files_s1 = glob.glob(os.path.join("s1" , "*/*.json"))
s1_df_from_each_file = (pd.read_json(f) for f in all_files_s1)
s1_df = pd.concat(s1_df_from_each_file, ignore_index=True)
s1_df.to_pickle("s1_df_raw.pkl")
s1_df = pd.read_pickle("s1_df_raw.pkl")


# In[8]:


s1_df = s1_df[["declaracion"]]


# In[9]:


declaracion = pd.json_normalize(s1_df.declaracion)


# In[11]:


del s1_df


# In[12]:


gc.collect()


# In[13]:


declaracion.to_pickle("s1_declaracion.pkl")


# In[10]:


declaracion

