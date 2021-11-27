#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:15:12 2021

@author: janinedevera
"""

import pandas as pd
from geopy.distance import geodesic
from fuzzywuzzy import fuzz

rdb = pd.read_csv("../data/requests_databasev1.csv")
sdb = pd.read_csv("../data/support_databasev1.csv")

## Matching
# Step 1: Create string for Category, Option, Date, Time

df_list = [rdb, sdb]

for df in df_list:
    df["string"] = df.iloc[:,2].astype(str) + df.iloc[:,3].astype(str) + df.iloc[:,4] + df.iloc[:,5].fillna('')

# Step 2: For each observation in rdb, calculate fuzz ratio with all observations in sdb

scores = []
for i in range(len(sdb)):
    



for col in rdb.columns:
    print(col)
    
    