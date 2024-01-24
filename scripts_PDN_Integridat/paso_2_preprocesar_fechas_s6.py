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
from tqdm import tqdm
tqdm.pandas()


# In[2]:


s6_df = pd.read_hdf("s6_hdf.h5")


# In[3]:


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
        


# In[4]:


s6_df.head()


# In[5]:


s6_df["earliest_contractPeriod_startDate"] = s6_df.contractPeriod_startDate.progress_apply(find_earliest_date)
s6_df["latest_contractPeriod_endDate"] = s6_df.contractPeriod_endDate.progress_apply(find_latest_date)


# In[10]:


s6_df = s6_df.drop(columns=["contractPeriod_startDate", "contractPeriod_endDate"])


# In[14]:


s6_df['earliest_contractPeriod_startDate'] = s6_df['earliest_contractPeriod_startDate'].progress_apply(lambda x: pd.to_datetime(x, utc=True))
s6_df['latest_contractPeriod_endDate'] = s6_df['latest_contractPeriod_endDate'].progress_apply(lambda x: pd.to_datetime(x, utc=True))

s6_df['earliest_contractPeriod_startDate'] = s6_df['earliest_contractPeriod_startDate'].dt.date
s6_df['latest_contractPeriod_endDate'] = s6_df['latest_contractPeriod_endDate'].dt.date


# In[15]:


s6_df


# In[16]:


s6_df.to_hdf("s6_hdf_dates.h5", key = "s6_df")

