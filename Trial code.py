# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:02:37 2021

@author: admin
"""

# Module 1
# login credentials
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.error = "Enter a valid username and password"
    def check(self):
        if (self.username == log_id and self.password == log_pass):
            print("Login successful")
        else:
            print(self.error)

log = Login("admin",  "admin")
log_id = input("Enter your user ID: ")
log_pass = input("Enter password: ")
log.check()

##############################################################################
import keyring as kr
import pandas as pd
import numpy as np

credentials_new = pd.DataFrame()
credentials_database = pd.read_csv("credentials_database.csv")

class NewUser:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
    
    def check(self):
        if (self.username %in% credentials_database$username):
            if (self.)
            
#############################################################################
import pickle
import time

def loaddict():
    try:
        with open("dictAcc.txt", "rb") as pkf:
            return pickle.load(pkf)
    except IOError:
        with open("dictAcc.txt", "w+") as pkf:
            pickle.dump(dict(), pkf)
            return dict()

def savedict(dictAcc):
    with open("dictAcc.txt", "wb") as pkf:
        pickle.dump(dictAcc, pkf)


def userPass():
    dictAcc = loaddict() #Load the dict
    checkAccount = raw_input("Do you have an account (Y or N)?")
    if (checkAccount == 'N' or checkAccount == 'n'):
        userName = raw_input("Please Set Your New Username: ")
        password = raw_input("Please Set Your New Password: ")
        if (userName in dictAcc):
            print("Username is taken")
            userPass()
        else:
            dictAcc[userName] = password 
            print("Congratulations! You have succesfully created an account!")
            savedict(dictAcc) #Save the dict
            time.sleep(1.5)
            # dataInput() Code ends
    elif(checkAccount == 'Y' or checkAccount == 'y'):
        login()
    else:
        print("Invalid answer, try again")
        userPass()


def login():
    global userName
    global password
    global tries
    loginUserName = raw_input("Type in your Username: ")
    loginPass = raw_input("Type in your Password: ")
    dictAcc = loaddict() #Load the dict
    if (tries < 3):
        for key in dictAcc:
            if (loginUserName == key and loginPass == dictAcc[key]):
                print("You have successfully logged in!")
                # dataInput() Code ends
            else:
                print("Please try again")
                tries += 1
                login()
            if (tries >= 3):
                print("You have attempted to login too many times. Try again later.")
                time.sleep(3)
                tries=1 #To restart the tries counter
                login()

global tries
tries=1
userPass()    

