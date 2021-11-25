# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 17:03:58 2021

@author: adellegia
"""

import csv
#import pandas as pd
import module_1_login_oop as m1
import module_2_requests_oop_dist as m2

def saveData():
    # Call Module 1
    user1 = m1.User()
    user1.checkAccount()
            
    # Run Module 2
    ### Ask if you want to add help request or support service
    print("\nHello, " + user1.getuserName() + "!" + "\nWelcome to GetHelp!")
    userType = str(input("What do you want to do today?" +
                         "\n1. Request for Help" + 
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))
    
    # add a unique requestID or offerID every time a user enters a new request
    # reqID =
    
    if userType == "1":
        Request1 = m2.Request("Help Request")
        Request1.runAll()
        
        
    # Module 3 (trial)
    ## either transform/reshape the dataframes to boolean or
    ## change saving format to boolean using the dictionary in Module 2 then match to columns    
        ### saves new request of user to dataframe
        with open("../data/requests_database.csv", 'a', encoding = 'UTF8', newline = '') as helpRequests:
            helpRequests_writer = csv.writer(helpRequests)
            helpRequests_writer.writerow([user1.getuserId(),
                                         userType,
                                         Request1.getreqDate(),
                                         Request1.getreqTime(), # must return time only
                                         Request1.getreqCat(),
                                         Request1.getreqOpt(),
                                         Request1.getreqOrg(),
                                         Request1.getreqDest()])
            
       ### saves new offer of user to dataframe
    elif userType == "2":
        Offer1 = m2.Request("Support Service") # can use request_OOP - if options for requests and offers are the same
        Offer1.runAll()
        
        with open("../data/support_database.csv", 'a', encoding = 'UTF8', newline = '') as supportServices:
            supportServices_writer = csv.writer(supportServices)
            supportServices_writer.writerow([user1.getuserId(),
                                         userType,
                                         Offer1.getreqDate(),
                                         Offer1.getreqTime(), # must return time only
                                         Offer1.getreqCat(),
                                         Offer1.getreqOpt(),
                                         Offer1.getreqOrg(),
                                         Offer1.getreqDest()])

saveData()  
  