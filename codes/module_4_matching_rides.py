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


## Cluster and match
# Level 1: Category, Option, and Date
    # try string matching
        # try Levenshtein or LongestCommonSubsequence - code from Lab below
class Levenshtein:
  def __init__(self, printoutput):
    self.po = printoutput

  def calculateDistance(self, s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
               
        return v1[len(t)]

  def printDistance(self, distance):
      print(self.po + str(distance))
      
class LongestCommonSubsequence:
  def __init__ (self, printoption):
    self.po = printoption

  def calculateDistance(self, s, t):

     
    # find the length of the strings
    m = len(s)
    n = len(t)
  
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
  
    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif s[i-1] == t[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]

  
  def printDistance(self, distance):
      print(self.po + str(distance))

# Level 2: Time (add range)

# Level 3: Distance