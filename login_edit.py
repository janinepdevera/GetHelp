# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 20:28:42 2021

@author: admin
"""

from sys import exit
import pandas as pd
import numpy as np
import csv

credentials_database = pd.read_csv("credentials_database.csv")

def LogIn():
    #if (checkAccount == 'Y' or checkAccount == 'y'):
        n1 = 0
        username = str(input("\nPlease enter your username: "))
        password = str(input("\nPlease enter your password: "))
        while ~((credentials_database[credentials_database.username == username]['password'] == password)[0]): # if exisitng username and wrong password only    
            n1 += 1
            if (n1 < 3):
                print("\nIncorrect username and password. Please enter your correct credentials.")
                username = str(input("\nPlease enter your username: "))
                password = str(input("\nPlease enter your password: "))
            if (n1 == 2):
                print("\nSorry, you have entered invalid username and password.")
                exit()
        print("\nYou have successfully logged in!")
        exit() # edit to go to Module 2


def NewUser():
    #if (checkAccount == 'N' or checkAccount == 'n'):            
        n2 = 0 
        username = str(input("Please enter your new username: "))
        #while (credentials_database.username.str.contains(str(username)).any()):
        while(len(credentials_database[credentials_database.username == username])):
            n2 += 1
            if (n2 < 3):
                print("\nUsername already exists. Please create a new account using a unique username.")
                username = str(input("\nPlease enter a unique username: "))
            if (n2 == 2):
                print("\nTry logging in instead")
                #exit() #edit to login function
                LogIn()
        password = str(input("\nPlease enter your password: ")) 
        
        with open("credentials_database.csv", 'a', encoding = 'UTF8', newline = '') as credentials:
            credentials_writer = csv.writer(credentials)
            credentials_writer.writerow(["000" + str(len(credentials_database) + 1),
                                        username, 
                                        password])
        LogIn()


def checkAccount():
    account = input("Do you already have a GetHelp account (Y or N)? ")
    if (account == 'Y' or account == 'y'): 
        LogIn()
    elif (account == 'N' or account == 'n'): 
        NewUser()
    else:
        print("\nPlease enter Y or N")

checkAccount()

##############################################################################

username = str(input("\nPlease enter your username: "))
password = str(input("\nPlease enter your password: "))
n = 0
x = credentials_database[credentials_database.username == username]['username'] 

def tripleCheck():
    n1 += 1
    if (n1 < 3):
        print("\nIncorrect username and password. Please enter your correct credentials.")
        username = str(input("\nPlease enter your username: "))
        password = str(input("\nPlease enter your password: "))
    if (n1 == 2):
        print("\nSorry, you have entered invalid username and password.")
        exit()

if len(x) == 0:
    ismissUsername = True
    while ~(credentials_database.username.str.contains(str(username)).any()):
        tripleCheck()
    print("\nYou have successfully logged in!")
    exit() # edit to go to Module 2          
elif len(x) == 1:
    while ~((credentials_database[credentials_database.username == username]['password'] == password)[0]):    
        tripleCheck()    
    print("\nYou have successfully logged in!")
    exit() # edit to go to Module 2



