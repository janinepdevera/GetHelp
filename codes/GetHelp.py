# -*- coding: utf-8 -*-
"""
Run GetHelp from Modules 1 to 4
"""

import module_1_login_oop as m1
import module_2_requests_oop as m2
import module_3_save_data as m3
import module_4_matching_oop as m4


def GetHelp():
    """
    A function that runs the workflow of the GetHelp program

    Returns
    -------
    All objects generated from functions inside

    """
    
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



