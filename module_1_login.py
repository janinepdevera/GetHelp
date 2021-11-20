# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:47:30 2021

@author: adellegia
"""

from sys import exit
import pandas as pd
#import numpy as np
import csv

cdb = pd.read_csv("credentials_database.csv")
username = str(input("Enter username: \n"))
password = str(input("Enter password: \n"))

user = (cdb[cdb.username == username]['username'] == username)
pw = (cdb[cdb.username == username]['password'] == password)


user.index
len(user.index) == 0

n1 = 0

if (len(user.index) == 0): # if username does not exist then error
    while (len(user.index) == 0):
        n1 += 1
        if (n1 < 3):
            print("\nIncorrect username and password. Please enter your correct credentials.\n")
            username = str(input("Enter username: \n"))
            password = str(input("Enter password: \n"))
        if (n1 == 2):
            print("Sorry, you have entered invalid username and password.\n")
            exit()
else:
    while ~(pw[pw.index[0]]): # while loop only works for exisitng usernames, edit further to unregistered usernames     
        n1 += 1
        if (n1 < 3):
            print("\nIncorrect username and password. Please enter your correct credentials.\n")
            username = str(input("Enter username: \n"))
            password = str(input("Enter password: \n"))
        if (n1 == 2):
            print("Sorry, you have entered invalid username and password.\n")
            exit()
    print("You have successfully logged in!\n")




def tryAgain(): # max 2 tries to log in
    n = n1
    n += 1
    if (n < 3):
        print("\nIncorrect username and password. Please enter your correct credentials.\n")
        username = str(input("Enter username: \n"))
        password = str(input("Enter password: \n"))
    if (n == 2):
        print("Sorry, you have entered invalid username and password.\n")
        exit()
 
        
  
    #tryAgain()
#print("You have successfully logged in!\n")
#exit()
while (len(user.index) == 1): 
    # if username exists and password is incorrect then check password
    while ~(pw[pw.index[0]]): # while loop    
        tryAgain()
    print("You have successfully logged in!\n")
    exit() # edit: go to Module 2
    
#################################################
def LogIn():
    cdb = pd.read_csv("credentials_database.csv")
    print("Please log in using your valid username and password to continue.\n")
    n1 = 0
    username = str(input("Enter username: \n"))
    password = str(input("Enter password: \n"))
     
    user = (cdb[cdb.username == username]['username'] == username)
    pw = (cdb[cdb.username == username]['password'] == password)
    
    while ~(pw[pw.index[0]]): # while loop only works for exisitng usernames, edit further to unregistered usernames     
        n1 += 1
        if (n1 < 3):
            print("\nIncorrect username and password. Please enter your correct credentials.\n")
            username = str(input("Enter username: \n"))
            password = str(input("Enter password: \n"))
        if (n1 == 2):
            print("Sorry, you have entered invalid username and password.\n")
            exit()
    print("You have successfully logged in!\n")
    exit() # edit: go to Module 2


def NewUser():
    cdb = pd.read_csv("credentials_database.csv")
    print("Register now as a new user to access GetHelp.\n")       
    n2 = 0 
    username = str(input("Please enter your new username: \n"))
        #while (credentials_database.username.str.contains(str(username)).any()):
    while(len(cdb[cdb.username == username])):
        n2 += 1
        if (n2 < 3):
            print("\nUsername already exists. Please create a new account using a unique username.\n")
            username = str(input("Please enter a unique username: \n"))
        if (n2 == 2):
            print("Try logging in instead. \n")
            LogIn()
    password = str(input("Please enter your password: \n"))
    print("Thank you for registering!\n")
        
    with open("credentials_database.csv", 'a', encoding = 'UTF8', newline = '') as credentials:
        credentials_writer = csv.writer(credentials)
        credentials_writer.writerow(["000" + str(len(cdb) + 1),
                                     username, 
                                     password])
    LogIn()


def checkAccount():
    account = input("Do you already have a GetHelp account (Y or N)? \n")
    if (account == 'Y' or account == 'y'): 
        LogIn()
    elif (account == 'N' or account == 'n'): 
        NewUser()
    else:
        print("\nPlease enter Y or N only. \n")
        checkAccount()

checkAccount()
    
