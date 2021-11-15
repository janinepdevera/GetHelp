#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 11:35:35 2021

@author: janinedevera
"""

### Module 2

# 1. Define OptionsSelect function (for all inputs that ask users to select from list of options)   

def OptionsSelect(options, name):
    index = 0
    indexValidList = []
    print('Select ' + name + ':')
    
        # 'options' is dictionary of categories to choose from 
    for optionName in options:
        index = index + 1
        indexValidList.extend([options[optionName]])
        print(str(index) + '. ' + options[optionName])
    inputValid = False
    
    while not inputValid:
        inputRaw = input(name + ': ')
        inputNo = int(inputRaw) - 1
        
        if inputNo > -1 and inputNo < len(indexValidList):
            selected = indexValidList[inputNo]
            print('Selected ' +  name + ': ' + selected)
            inputValid = True
            break
        else:
            print('Please select a valid ' + name + ' number')
    
    return selected


# 2. Select a Help Category (using OptionsSelect function)

helpCategory = {"1": "Errands",
                "2": "Ride",
                "3": "Translate",
                "4": "Tutor"}

hcategory = OptionsSelect(helpCategory, "Help Category")

# 3. Create nested dictionionary for category options

optionsDict = {"Errands": {"1": "Flat maintenance",
                            "2": "Government services",
                            "3": "Grocery shopping",
                            "4": "Mall shopping",
                            "5": "Move in/out",
                            "6": "Take care of pets/plants"},
                "Ride": {"1": "Charlottenburg",
                         "2": "Friedrichshain",
                         "3": "Kreuzberg",
                         "4": "Litchtenberg",
                         "5": "Mitte",
                         "6": "Neukoelln",
                         "7": "Pankow",
                         "8": "Spandau",
                         "9": "Steglitz",
                         "10": "Tempelhof",
                         "11": "Schoeneberg",
                         "12": "Treptow-Koepenick"},
                "Translate": {"1": "English",
                              "2": "French",
                              "3": "German",
                              "4": "Hindi",
                              "5": "Japanese",
                              "6": "Mandarin",
                              "7": "Polish",
                              "8": "Russian",
                              "9": "Spanish",
                              "10": "Swedish"},
                "Tutor": {"1": "Economics",
                          "2": "Finance",
                          "3": "History",
                          "4": "Law",
                          "5": "Literature",
                          "6": "Mathematics",
                          "7": "Programming Language: Python",
                          "8": "Programming Language: R",
                          "9": "Statistics",
                          "10": "Sciences"}
                         }

# 4. Select option based on selected Help Category 

helpOptions = optionsDict[hcategory]

hoption = OptionsSelect(helpOptions, "option")

# 5. Select date and time for Help Category

from datetime import datetime

def validate():   
    
    # while loop for date
    while True:
        try:
            requestdate = datetime.strptime(input("What date do you need help? (YYYY-MM-DD): ") ,'%Y-%m-%d')
            if requestdate < datetime.now():
                print("Invalid date. Please enter a future date.")
                continue
        except ValueError:
            print ("Invalid date. Please enter date in YYYY-MM-DD format.") 
            continue
        else:
            
            #while loop for time
            while True: 
                try:
                    requesttime = datetime.strptime(input("What time do you need help? (HH:MM): "), "%H:%M")
                except ValueError:
                    print ("Invalid time. Please enter date in HH:MM format.") 
                    continue
                else: 
                    break
            break
    
    print("Thank you! Your request has been recorded.")

date = validate()


