#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 00:28:45 2021

@author: janinedevera
"""

from datetime import datetime

class Request:
    def __init__(self, selectCat="", selectOption="",requestdate="", requesttime=""): 
        self.selectCat = selectCat
        self.selectOption = selectOption
        self.requestdate = requestdate
        self.requesttime = requesttime
        
        self.Category = {"1": "Errands",
                    "2": "Ride",
                    "3": "Translate",
                    "4": "Tutor"}
      
        self.optionsDict = {"Errands": {"1": "Flat maintenance",
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
    
        
    def CatSelect(self):
      self.selectCat = self.OptionsSelect(self.Category, "Category")
          
    def OptSelect(self):
        self.catOptions = self.optionsDict[self.selectCat]
        self.selectOption= self.OptionsSelect(self.catOptions, "Option")
        
    # need to combine the strings for date and time after input (or print time without the date string)
    def validDate(self):   
        while True:
            try:
                self.requestdate = datetime.strptime(input("What date do you need help? (YYYY-MM-DD): ") ,'%Y-%m-%d')
                if self.requestdate < datetime.now():
                    print("Invalid date. Please enter a future date.")
                    continue
            except ValueError:
                print ("Invalid date. Please enter date in YYYY-MM-DD format.") 
                continue
            break
     
    def validTime(self):   
        while True: 
            try:
                self.requesttime = datetime.strptime(input("What time do you need help? (HH:MM): "), "%H:%M")
            except ValueError:
                print ("Invalid time. Please enter date in HH:MM format.") 
                continue
            else: 
                break
    
    def printDetails(self):
        print("Thank you! Your request has been recorded with the following details:")
        print("Category: ", self.selectCat)
        print("Option: ", self.selectOption)

    # getters
    def getreqCat(self):
        return self.selectCat
    
    def getreqOpt(self):
        return self.selectOption
    
    def getreqDate(self):
        return self.requestdate.date()
        
    def getreqTime(self):
        return self.requesttime.time()
    
