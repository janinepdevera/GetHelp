# -*- coding: utf-8 -*-
"""
Module 3: Save the Data

The User's request or support details are saved in dataframes.
"""

import csv
import module_1_login_oop as m1
import module_2_requests_oop as m2
import pandas as pd


def transID(df,user1):
    """
    Enter valid ID for user
    
    Parameters
    -------
    df: dataframe
        A dataframe of requests/support
    user1: class
        Name of class User  
    
    Returns
    -------
    reqid: str
        A unique Transaction ID assigned to a request or support added by a User
    """
    
    try:
        reqID = 1 + df[df.username == user1.getuserName()].groupby('userID')['username'].value_counts().tolist()[0]
        reqID = m1.idFormat(str(reqID))
    except IndexError:
        reqID = m1.idFormat("1")
    return reqID
    
def saveData():
    """
    Saves the inputs of User in the Class Request
    

    Returns
    -------
    A dataframe in csv format of requests/support

    """
    
    
    user1 = m1.User()
    rdb = pd.read_csv("../data/requests_database.csv", dtype = {"transactionID": "str", "userID": "str", "helpID": "str"})
    sdb = pd.read_csv("../data/support_database.csv", dtype = {"transactionID": "str", "userID": "str", "helpID": "str"})

    user1.checkAccount()
            
    print("\nHello, " + user1.getuserName() + "!" + "\nWelcome to GetHelp!")
    userType = str(input("What do you want to do today?" +
                         "\n1. Request for Help" + 
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))
    # Input Request   
    if userType == "1":
        Request1 = m2.Request("Help Request")
        Request1.runAll()
        
        reqID = transID(rdb, user1)
        transactionID = user1.getuserId() + str(userType) + reqID # 11-digit transaction id
        print("\nPlease check the status of your GetHelp Request using your transaction id.",
              "\n Transaction ID: ", transactionID,
              "\n",
              "\nThank you for using GetHelp, ", user1.getuserName(), "!",
              "\nHave a nice day!")
        
        with open("../data/requests_database.csv", 'a', encoding = 'UTF8', newline = '') as helpRequests:
            helpRequests_writer = csv.writer(helpRequests)
            helpRequests_writer.writerow([transactionID,
                                         user1.getuserId(),
                                         user1.getuserName(),
                                         userType,
                                         reqID,
                                         Request1.getreqDate(),
                                         Request1.getreqTime(), 
                                         Request1.getreqCat(),
                                         Request1.getreqOpt(),
                                         Request1.getreqOrg(),
                                         Request1.getreqOrg_add(),
                                         Request1.getreqOrg_coord(),
                                         Request1.getreqDest(),
                                         Request1.getreqDest_add(),
                                         Request1.getreqDest_coord(),
                                         Request1.getreqInfo(),
                                         Request1.getTimestamp()])
    
    # Input Offer        
    elif userType == "2":
        Offer1 = m2.Request("Support Service") 
        Offer1.runAll()
        
        reqID = transID(sdb, user1)
        transactionID = user1.getuserId() + str(userType) + reqID # 11-digit transaction id
        print("\nPlease check the status of your GetHelp Offer using your transaction id.",
              "\n Transaction ID: ", transactionID,
              "\n",
              "\nThank you for using GetHelp, ", user1.getuserName(), "!",
              "\nHave a nice day!")
        
        with open("../data/support_database.csv", 'a', encoding = 'UTF8', newline = '') as supportServices:
            supportServices_writer = csv.writer(supportServices)
            supportServices_writer.writerow([transactionID,
                                         user1.getuserId(),
                                         user1.getuserName(),
                                         userType,
                                         reqID,
                                         Offer1.getreqDate(),
                                         Offer1.getreqTime(), 
                                         Offer1.getreqCat(),
                                         Offer1.getreqOpt(),
                                         Offer1.getreqOrg(),
                                         Offer1.getreqOrg_add(),
                                         Offer1.getreqOrg_coord(),
                                         Offer1.getreqDest(),
                                         Offer1.getreqDest_add(),
                                         Offer1.getreqDest_coord(),
                                         Offer1.getreqInfo(),
                                         Offer1.getTimestamp()])

    else:
        print("\nPlease enter a valid option.")
        saveData()
