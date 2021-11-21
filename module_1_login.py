# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:47:30 2021

@author: adellegia
"""

from sys import exit
import pandas as pd
import csv
#import module_2_requests_oop_AA
#import module_2_offers_oop_AA 

def LogIn():
    cdb = pd.read_csv("credentials_database.csv")
    print("\nPlease log in using your valid username and password.\n")

    username = str(input("Enter username: \n"))
    n1 = 0
    n2 = 0
    index = cdb.index
        
    while (len((cdb[cdb.username == username]['username'] == username).index) == 0):
        n1 += 1
        if (n1 < 3):
            print("\nInvalid username. Please enter an existing username.\n")
            username = str(input("Enter username: \n"))
        else:
            print("Sorry, you have entered an invalid username. Try creating a new account instead.\n")
            exit()
    else:
       #print("\nUsername is valid.")
       ind = index[cdb.username == username].tolist()
       password = str(input("\nEnter password: \n"))
       while ~((cdb.password[ind] == password)[ind[0]]): 
           n2 += 1
           if (n2 < 3):
                print("\nIncorrect password. Please enter your correct credentials.\n")
                print("Username:\n" + username)
                password = str(input("Enter password: \n"))
           else:
                print("Sorry, you have entered an invalid password.\n")
                exit()
       print("\nYou have successfully logged in!\n")
       #userid = cdb.userid[ind]
       #return userid
   # go to MODULE 2

def NewUser():
    cdb = pd.read_csv("credentials_database.csv")
    print("\nRegister now as a new user to access GetHelp!\n")       
    n3 = 0 
    username = str(input("Please enter your new username: \n"))
    while(len(cdb[cdb.username == username])):
        n3 += 1
        if (n3 < 3):
            print("\nUsername already exists. Please create a new account using a unique username.\n")
            username = str(input("Please enter a unique username: \n"))
        if (n3 == 2):
            print("Try logging in instead. \n")
            LogIn()
    password = str(input("Please enter your password: \n"))
    print("\nThank you for registering!\n")
    
    userid = str(len(cdb) + 1) #5-digit userid
    if len(userid) == 1:
        userid = "0000" + userid
    elif len(userid) == 2:
        userid = "000" + userid
    elif len(userid) == 3:
        userid = "00" + userid
    elif len(userid) == 4:
        userid = "0" + userid
    
    with open("credentials_database.csv", 'a', encoding = 'UTF8', newline = '') as credentials:
        credentials_writer = csv.writer(credentials)
        credentials_writer.writerow([userid, 
                                     username, 
                                     password])
    LogIn()
    return userid

def checkAccount():
    account = input("Do you already have a GetHelp account?" + 
                    "\n1. Yes" +
                    "\n2. No" +
                    "\nEnter 1 or 2: ")
    if (account == "1"): 
        LogIn()
    elif (account == "2"): 
        NewUser()
    else:
        print("\nPlease enter a valid option.\n")
        checkAccount()
        
def getuserId():
    cdb = pd.read_csv("credentials_database.csv")
    index = cdb.index
    #ind = len((cdb.username == username).index.tolist())-1
    ind = index[cdb.username == username].tolist()
    userid = cdb.userid[ind]
    
checkAccount()

index[cdb.username == "adelle"].tolist()