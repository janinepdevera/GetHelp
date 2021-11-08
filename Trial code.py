# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:02:37 2021

@author: admin
"""

# Module 1
# login credentials
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.error = "Enter a valid username and password"
    def check(self):
        if (self.username == log_id and self.password == log_pass):
            print("Login successful")
        else:
            print(self.error)

log = Login("admin",  "admin")
log_id = input("Enter your user ID: ")
log_pass = input("Enter password: ")
log.check()

