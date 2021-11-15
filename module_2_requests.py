#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 11:35:35 2021

@author: janinedevera
"""

### Module 2


# 2. Create class "Category:

class Category:
    def __init__(self, name, option):
        self.name = category
        self.option = option
        
    def OptionsSelect(self, options, name):
        index = 0
        indexValidList = []
        print('Select ' + name + ':')
    
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



# Sample functions

# 1. Define OptionsSelect function (for all inputs that ask users to select from list of options)   

def OptionsSelect(options, name):
    index = 0
    indexValidList = []
    print('Select ' + name + ':')
    
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

options = {"1": "Errands",
           "2": "Ride",
           "3": "Translate",
           "4": "Tutor"}

category = OptionsSelect(options, "Help Category")

# 3. Create nested dictionionary for category options

optionsDict = {"Errands": {"1": "Flat maintenance",
                            "2": "Government services",
                            "3": "Grocery shopping",
                            "4": "Mall shopping",
                            "5": "Move in/out",
                            "6": "Take care of pets/plants"},
                "Ride": {"1": "Berlin-Mitte",
                         "2": "Charlottenburg",
                         "3": "Prenzlauer Berg",
                         "4": "Friedrichshain",
                         "5": "Kreuzberg"},
                "Translate": {"1": "English",
                              "2": "Chinese",
                              "3": "French",
                              "4": "German",
                              "5": "Japanese",
                              "6": "Polish"},
                "Tutor": {"1": "Economics",
                          "2": "English",
                          "3": "History",
                          "4": "Law",
                          "5": "Mathematics",
                          "6": "Statistics",
                          "7": "Sciences"}
                         }

# 4. Select option based on selected Help Category 

options = optionsDict[category]

HelpOption = OptionsSelect(options, "option")
