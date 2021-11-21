# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:03:58 2021

@author: adellegia
"""

import csv
import pandas as pd
import module_1_login_oop as m1
import module_2_requests_oop_AA as m2

# 1. Module 1
user1 = m1.User()
def checkAccount():
    account = input("Do you already have a GetHelp account?" + 
                    "\n1. Yes" +
                    "\n2. No" +
                    "\nEnter 1 or 2: ")
    if (account == "1"): 
        user1.LogIn()
    elif (account == "2"): 
        user1.NewUser()
    else:
        print("\nPlease enter a valid option.\n")
        checkAccount()

checkAccount()    

# 2. Module 2
### Ask if you want to add help request or support service
print("\nHello, " + user1.getuserName() + "!" + "\nWelcome to GetHelp!")
userType = str(input("What do you want to do today?" +
                     "\n1. Request for Help" + 
                     "\n2. Offer to Help\n" +
                     "\nEnter 1 or 2: "))

Request1 = m2.Request()
if userType == "1":
    Request1.CatSelect()
    Request1.OptSelect()
    Request1.validDate()
    Request1.validTime()
    Request1.printDetails()
    
# 3. Module 3 (trial)
    ### saves new request of user to dataframe
        ### change to boolean use dictionary in Module2 and match with columns
    with open("requests_database.csv", 'a', encoding = 'UTF8', newline = '') as helpRequests:
        helpRequests_writer = csv.writer(helpRequests)
        helpRequests_writer.writerow([user1.getuserId(),
                                     Request1.getreqDate(),
                                     Request1.getreqTime(), # must return time only
                                     Request1.getreqCat(),
                                     Request1.getreqOpt()])
        
   ### saves new support of user to dataframe
#elif userType == "2":
    
    