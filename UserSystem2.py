# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:09:30 2016

@author: GY
"""
import sys
import numpy
import os




#Function to read in log file, and parse data into 2D list.
def ReadLog(filepath):
    DataList=[]
    with open(filepath,'a') as UG:
        if os.stat(filepath).st_size==0:
            UG.write("User\tPassword\tRecord")
    with open(filepath,'r') as FP:              #Parse the log file into list.
        for line in FP:
            if line.strip()=='':
                continue
            DataList.append(line.strip().split('\t'))
    return DataList


def CreateLog(DataList,filepath):
    with open(filepath,'w') as UG:
        for i in range(len(DataList)):
            for j in range(len(DataList[0])-1):
                UG.write(DataList[i][j]+'\t')
            UG.write(DataList[i][-1]+'\n')
        UG.write('\b')


#Function to find user.
def FindUser(filepath,UserName):
    Data=ReadLog(filepath)
    for i in range(1,len(Data)):
        if UserName==Data[i][0]:
            return i
    return 0


#Function to add a new user.
def AddUser(filepath):
    UserName=input("Please input your username:")   #Input username.
    num=0
    while UserName=='':                     #Ensure username not empty.
        num+=1
        if num>3:
            print("Username not created. Please register again later!")
        UserName=input("Username cannot be empty! Please input your username:")
    num=0
    while FindUser(filepath,UserName):     #Check if username has been used. If not, FindUser returns False.
        num+=1
        if num>3:
            print("Username not created. Please register again later!")
            return
        UserName=input("The username has been used, please choose another username:")
    Password=input("Please input your password:")
    num=0
    while Password=='':         #Ensure a non-empty password.
        num+=1
        if num>3:
            print("Password not created. Please register again later!")
            return ''
        Password=input("Password cannot be empty! Please input your password:")
    PwdConfirm=input("Please re-type your password:")
    num=0         #3 times of confirmation trials; fail after 3 times.
    while PwdConfirm!=Password:
        num+=1
        if num>3:
            print("Password not created. Please register again later!")
            return ''
        PwdConfirm=input("Password inputs are not the same. Please re-type your password:")
    with open(filepath,'a') as UG:
        UG.write('\n'+UserName+'\t'+Password+'\t0')
    print("Thank you for registering! Your info has been saved.")
    return UserName


#Function to print log file in clear format.
def PrintLog(filepath):
    DataList=numpy.array(ReadLog(filepath))    
    col=len(DataList[0])
    length=[]
    for i in range(col):
        length.append(0)
    for i in range(col):
        for j in range(len(DataList)):
            if length[i]<len(DataList[j][i]):
                length[i]=len(DataList[j][i])
    for i in range(len(DataList)):
        for j in range(len(DataList[0])):
            print(DataList[i][j].ljust(length[j]),end='   ')
        print()


#Function to print log to user; passwords for other users are shown as'******'.
def VisitLog(filepath,UserName):
    DataList=numpy.array(ReadLog(filepath))    
    col=len(DataList[0])
    index=FindUser(filepath,UserName)
    for i in range(len(DataList[0])):
        if DataList[0][i]=='Password':
            PwdCol=i
    Pwd=DataList[index,PwdCol]
    for i in range(1,len(DataList)):
        DataList[i,PwdCol]='******'
    DataList[index,PwdCol]=Pwd
    length=[]
    for i in range(col):
        length.append(0)
    for i in range(col):
        for j in range(len(DataList)):
            if length[i]<len(DataList[j][i]):
                length[i]=len(DataList[j][i])
    for i in range(len(DataList)):
        for j in range(len(DataList[0])):
            print(DataList[i][j].ljust(length[j]),end='   ')
        print()


#Function to write entries of users into blacklist.
def BlackList(filepath,UserName):
    DataList=ReadLog(filepath)
    with open('BlackList.log','a') as UG:           #Test empty: if so, then write title.
        if os.stat('BlackList.log').st_size==0:
            UG.write("User\tPassword\tRecord")
    index=FindUser(filepath,UserName)           #Locate user.
    for i in range(len(DataList[0])):           #Locate password and record columns.
        if DataList[0][i]=='Password':
            PwdCol=i
        elif DataList[0][i]=='Record':
            RecCol=i
    Password=DataList[index][PwdCol]
    Record=DataList[index][RecCol]
    with open('BlackList.log','a') as UG:
        UG.write('\n'+UserName+'\t'+Password+'\t'+Record)   #Write in.

#Function to login or register.
def LogIn(filepath):
    UserName=input("Welcome to log in!\nUsername:")
    num=0
    while not FindUser(filepath,UserName):         #Re-enter or register username, if existing ones not found.
        num+=1
        if num>3:
            pin=input("Login failed. Do you want to register?(Y/N)")        #Register.
            if pin=='Y' or pin=='y':
                AddUser(filepath)
                print("Please login anther time.")
                return
            else:
                print("Username not exist. Please try another time!")
                return
        UserName=input("Username not exist; please re-enter username.\nUsername:")
    index=FindUser(filepath,UserName)       #Track position of the username in file.
    DataList=ReadLog(filepath)
    for i in range(len(DataList[0])):
        if DataList[0][i]=='Password':
            PwdCol=i
        elif DataList[0][i]=='Record':
            RecCol=i
    Counter=int(DataList[index][RecCol])
    if Counter>2:
        print("Sorry! Your account has been locked!")
        return 0
    Password=input("Password:")
    while Password!=DataList[index][PwdCol]:
        Counter+=1
        DataList[index][RecCol]=str(Counter)
        if Counter>2:
            CreateLog(DataList,filepath)
            BlackList(filepath,UserName)
            print("Sorry! You've tried over 3 times, and your account is locked!")
            return 0
        Password=input("Wrong password! You have "+str(3-Counter)+" times to enter password.\nPassword:")
    CreateLog(DataList,filepath)
    print("Login succesful!")
    VisitLog(filepath,UserName)



def main():
    if __name__==__main__:
        LogIn('userlog.log')
        
        