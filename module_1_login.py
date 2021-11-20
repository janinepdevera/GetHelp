# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:47:30 2021

@author: adellegia
"""

from sys import exit
import pandas as pd
#import numpy as np
import csv


def LogIn():
    cdb = pd.read_csv("credentials_database.csv")
    print("Please log in using your valid username and password.\n")

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
       print("\nThe username exists.\n")
       ind = index[cdb.username == username].tolist()
       password = str(input("Enter password: \n"))
       while ~((cdb.password[ind] == password)[ind[0]]): 
           n2 += 1
           if (n2 < 3):
                print("\nIncorrect password. Please enter your correct credentials.\n")
                print("Username:\n" + username)
                password = str(input("Enter password: \n"))
           else:
                print("Sorry, you have entered an invalid password.\n")
                exit()
       print("You have successfully logged in!\n")
       exit() # go to MODULE 2

def NewUser():
    cdb = pd.read_csv("credentials_database.csv")
    print("Register now as a new user to access GetHelp.\n")       
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
    print("Thank you for registering!\n")
        
    with open("credentials_database.csv", 'a', encoding = 'UTF8', newline = '') as credentials:
        credentials_writer = csv.writer(credentials)
        credentials_writer.writerow(["000" + str(len(cdb) + 1),
                                     username, 
                                     password])
    LogIn()


def checkAccount():
    account = input("Do you already have a GetHelp account?\n(Y or N)? \n")
    if (account == 'Y' or account == 'y'): 
        LogIn()
    elif (account == 'N' or account == 'n'): 
        NewUser()
    else:
        print("\nPlease enter Y or N only. \n")
        checkAccount()

checkAccount()
    
