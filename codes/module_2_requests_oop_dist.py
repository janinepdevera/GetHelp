#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 00:28:45 2021

@author: janinedevera
"""

from datetime import datetime 
from datetime import date 

class Request:
    def __init__(self, type):
        self.type = type
        
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
    
    # general function for selecting from dictionary    
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
    
    # select category    
    def CatSelect(self):
      self.selectCat = self.OptionsSelect(self.Category, self.type)
    
    # select option
    def OptSelect(self):
        if self.selectCat != "Ride":
            self.catOptions = self.optionsDict[self.selectCat]
            self.selectOption= self.OptionsSelect(self.catOptions, (self.type + " Option"))            
        else:
            self.selectOption = "NA"
    
    # select option
    def LocSelect(self):
        if self.selectCat == "Ride":
            self.OptOrg = input("Please enter the complete address of your origin: ")
            self.OptDest = input("Please enter the complete address of your destination: ")
        else:
            self.OptOrg = "NA"
            self.OptDest = "NA"
    
    # input date    
    def validDate(self):   
        while True:
            try:
                self.requestdate = datetime.date(datetime.strptime(input("Enter date for request (YYYY-MM-DD): ") ,'%Y-%m-%d'))
                if self.requestdate < date.today():
                    print("Invalid date. Please enter a future date.")
                    continue
            except ValueError:
                print ("Invalid date. Please enter date in YYYY-MM-DD format.") 
                continue
            break
    
    # input time 
    def validTime(self):   
        while True: 
            try:
                self.requesttime = datetime.time(datetime.strptime(input("Enter time for request (HH:MM): "), "%H:%M"))
            except ValueError:
                print ("Invalid time. Please enter date in HH:MM format.") 
                continue
            else: 
                break
    
    # print request details
    def printDetails(self):
        print("Thank you! Your", self.type, "has been recorded with the following details:")
        print("Category: ", self.selectCat)
        print("Option: ", self.selectOption)
        print("Origin: ", self.OptOrg)
        print("Destination: ", self.OptDest)
        print("Date: ", self.requestdate)
        print("Time: ", self.requesttime)
    
    def runAll(self):
        self.CatSelect()
        self.OptSelect()
        self.LocSelect()
        self.validDate()
        self.validTime()
        self.printDetails()
    
    # getters
    def getreqCat(self):
        return self.selectCat
    
    def getreqOpt(self):
        return self.selectOption
    
    def getreqOrg(self):
        return self.OptOrg
    
    def getreqDest(self):
        return self.OptDest
    
    def getreqDate(self):
        return self.requestdate
        
    def getreqTime(self):
        return self.requesttime

