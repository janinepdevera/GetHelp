# -*- coding: utf-8 -*-
"""
Module 1: Log-in

A User is asked to either log in using their credentials or create a new account.
"""

from sys import exit
import pandas as pd
import time
import csv
import base64


def idFormat(id_num):
    """Format a numeric id into 5-digit string.
    
    Paramters
    ---------
    id_num: str
        A unique string number assigned to a User or Request.    
    """
    
    if len(id_num) == 1:
        id_num = "0000" + id_num
    elif len(id_num) == 2:
        id_num = "000" + id_num
    elif len(id_num) == 3:
        id_num = "00" + id_num
    elif len(id_num) == 4:
        id_num = "0" + id_num
    return id_num

class User:
    """
    A class used to represent a User.  
    
    Attributes
    ----------
    cdb: dataframe
        The dataframe of all users' login credentials
    username: str
        The unique login name of the User
    password: str
        The login password of the User
    pw_encrypt: str
        The encrypted login password of the User
    userid: str
        The unique id of the User
    index: range
        The index range of cdb dataframe
        
    Methods
    -------
    LogIn()
        Allows User to log in
    NewUser()
        Creates a new user account
    checkAccount()
        Checks if User has an account 
    getuserId()
        Prints the userid
    getuserName()
        Prints the username
    """
    
    def __init__(self, cdb = pd.DataFrame(), username="", password="", pw_encrypt="", userid = "", index = ""):
        """Constructs objects of class User.        

        Parameters
        ----------
        cdb : dataframe
            Login credentials dataframe. The default is pd.DataFrame().
        username : str
            Input username. The default is "".
        password : str
            Input password. The default is "".
        pw_encrypt : str
            Encrpyt password. The default is "".
        userid : str
            Unique userid. The default is "".
        index : range
            Index range of cdb dataframe. The default is "".
        """
        
        self.cdb = cdb
        self.username = username
        self.__password = password
        self.__pw_encrypt = pw_encrypt
        self.userid = userid
        self.index = index
        
    def LogIn(self):
        """Allows existing User to log in using username and password.

        Returns
        -------
        None.
        """
        
        self.cdb = pd.read_csv("../data/credentials_database.csv")
        print("\nPlease log in using your valid username and password.\n")
    
        self.username = str(input("Enter username: \n"))
        self.index = self.cdb.index
        n1 = 0
        n2 = 0 
            
        while (len((self.cdb[self.cdb.username == self.username]['username'] == self.username).index) == 0):
            n1 += 1
            if (n1 < 3):
                print("\nInvalid username. Please enter an existing username.\n")
                self.username = str(input("Enter username: \n"))
            else:
                print("Sorry, you have entered an invalid username. Try creating a new account instead.\n")
                time.sleep(2)
                exit()
        else:
           ind = self.index[self.cdb.username == self.username].tolist()
           self.password = str(input("\nEnter password: \n"))
           self.pw_encrypt = base64.b64encode(self.password.encode("utf-8")).decode()
           while ~((self.cdb.password[ind] == self.pw_encrypt)[ind[0]]): 
               n2 += 1
               if (n2 < 3):
                    print("\nIncorrect password. Please enter your correct credentials.\n")
                    print("Username:\n" + self.username)
                    self.password = str(input("Enter password: \n"))
                    self.pw_encrypt = base64.b64encode(self.password.encode("utf-8")).decode()
               else:
                    print("Sorry, you have entered an invalid password.\n")
                    time.sleep(2)
                    exit()
               break
           print("\nYou have successfully logged in!\n")
           ## need to debug this to continue to Module 2 (i.e. after 3 username exists then login)
        #while True:
            #pass
        
    def NewUser(self):
        """Creates a new user account.
        Saves new user's login credentials to cdb dataframe.
        Asks new user to log in after.

        Returns
        -------
        None.

        """
        
        self.cdb = pd.read_csv("../data/credentials_database.csv")
        print("\nRegister now as a new user to access GetHelp!\n")       
        n3 = 0 
        self.username = str(input("Please enter your new username: \n"))
        while(len(self.cdb[self.cdb.username == self.username])):
            n3 += 1
            if (n3 < 3):
                print("\nUsername already exists. Please create a new account using a unique username.\n")
                self.username = str(input("Please enter a unique username: \n"))
            #if (n3 == 2):
            else:
                print("Try logging in instead. \n")
                User.LogIn(self)
        self.password = str(input("Please enter your password: \n"))
        self.pw_encrypt = str(base64.b64encode(self.password.encode("utf-8")).decode())
        print("\nThank you for registering!\n")
        
        self.userid = idFormat(str(len(self.cdb) + 1)) #5-digit userid
         
        with open("../data/credentials_database.csv", 'a', encoding = 'UTF8', newline = '') as credentials:
            credentials_writer = csv.writer(credentials)
            credentials_writer.writerow([self.userid, 
                                         self.username, 
                                         self.pw_encrypt])
        User.LogIn(self)
    
    def checkAccount(self):
        """Asks if User has an existing account.
        If has an account, User will log in.
        If has no account, User will create a new account.

        Returns
        -------
        None.

        """
        account = input("Do you already have a GetHelp account?" + 
                        "\n1. Yes" +
                        "\n2. No" +
                        "\nEnter 1 or 2: ")
        if (account == "1"): 
            User.LogIn(self)
        elif (account == "2"): 
            User.NewUser(self)
        else:
            print("\nPlease enter a valid option.\n")
            User.checkAccount(self)    
       
    def getuserId(self):
        """Prints the userid of the User

        Returns
        -------
        userid: str
            The unique id of the User           
        """
        
        self.cdb = pd.read_csv("../data/credentials_database.csv")
        ind = self.index[self.cdb.username == self.username].tolist()
        self.userid = idFormat(str(self.cdb.userid[ind[0]]))
        return(self.userid)
 

    def getuserName(self):
        """Prints the username of the User.
        
        Returns
        -------
        username: str
            The unique name of the User
        """
        return self.username
    
    
    
