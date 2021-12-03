# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 19:52:10 2021

@author: admin
"""

import module_1_login_oop as m1
import module_2_requests_oop as m2
import module_3_save_data as m3
import module_4_matching_oop_AA as m4


def GetHelp():
    Match = m4.Matches()
    action = str(input("Guten Tag! Welcome to GetHelp!" +
              "\nAre you here to: " + 
              "\n1. Add Request/Offer" +
              "\n2. Check status of Request/Offer?" + 
              "\nEnter 1 or 2: "))
    
    if action == "1":
        m3.saveData()
    elif action == "2":      
        Match.runAll()
    else:
        print("\nPlease enter a valid option.")
        GetHelp()
        
GetHelp()



