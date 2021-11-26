# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 17:13:25 2021

@author: adellegia
"""
import pandas as pd
from geopy.distance import geodesic

rdb = pd.read_csv("../data/requests_databasev1.csv")
sdb = pd.read_csv("../data/support_databasev1.csv")

#a = (geo(rdb.reqOrgAdd[1]).latitude, geo(rdb.reqOrgAdd[1]).longitude)
#b = (geo(rdb.reqDestAdd[1]).latitude, geo(rdb.reqDestAdd[1]).longitude)

a = rdb.reqOrgCoord[1].strip('()').split(',')
a = tuple(a)
a = (float(a[0]), float(a[1]))


b = rdb.reqDestCoord[1].strip('()').split(',')
b = tuple(b)
b = (float(b[0]), float(b[1]))

geodesic(a, b).kilometers
geodesic(a, b).miles
