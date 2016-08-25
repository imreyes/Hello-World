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
        if os.stat(filepath).st_size==0:                #Create title if the file is empty (newly created).
            UG.write("User\tPassword\tRecord")
    with open(filepath,'r') as FP:                      #Parse the log file into list.
        for line in FP:
            if line.strip()=='':                        #Jump over empty lines.
                continue
            DataList.append(line.strip().split('\t'))   #Write the data from file to list; eliminate all '\n's and spaces.
    return DataList


'''Function to "refresh" the log file when there's an update in the middle of data. Am not sure how would people locate data
in the middle of a file and edit - only knows 'a' to edit file starting from the end of it.'''
def CreateLog(DataList,filepath):                       #Overwrite the whole file according to the content in the list.
    with open(filepath,'w') as UG:
        for i in range(len(DataList)):
            for j in range(len(DataList[0])-1):         #As the last column (DataList[x][-1]) is not followed by '\t' but '\n', the inner
                UG.write(DataList[i][j]+'\t')           #loop will stop at the last but one column, and the last one is written-in separately.
            UG.write(DataList[i][-1]+'\n')
        UG.write('\b')                                  #Used to delete the '\n' at the very end of the file; this line and line22 together ensure the right
                                                        #format of the file (otherwise there will be a DataList[x]=[''], and DataList[x][1] willl have problem.


#Function to find user.
def FindUser(filepath,UserName):                        #I'm surprised I couldn't find a simple function in list type to search content and return index.
    Data=ReadLog(filepath)
    for i in range(1,len(Data)):
        if UserName==Data[i][0]:
            return i
    return 0


#Function to add a new user.
def AddUser(filepath):
    UserName=input("Please input your username:")   #Input username.
    num=0
    while UserName=='':                     #Ensure username not empty. Can be improved: ask if user wants to register after 1st wrong name.
        num+=1
        if num>3:
            print("Username not created. Please register again later!")
        UserName=input("Username cannot be empty! Please input your username:")
    num=0
    while FindUser(filepath,UserName):     #Check if username has been used. If not, FindUser returns False.
        num+=1                              #Have used too many identical structure - stop after 3 trials.
        if num>3:
            print("Username not created. Please register again later!")
            return
        UserName=input("The username has been used, please choose another username:")
    Password=input("Please input your password:")                           #Could improve: show up only '*' but the last letter when typing password.
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
        UG.write('\n'+UserName+'\t'+Password+'\t0')                 #Write in info for new user; the '0' in last column is a recorder counting times of wrong password when logging in of this user.
    print("Thank you for registering! Your info has been saved.")
    return UserName


#Function to print log file in clear format.
def PrintLog(filepath):                                     #This prints out all passwords!
    DataList=numpy.array(ReadLog(filepath))    
    col=len(DataList[0])
    length=[]                                               #Find the proper length for each column.
    for i in range(col):                                    #Get the column numbers, to store length for each column in a list.
        length.append(0)
    for i in range(col):                                    #Find the longest string in each column, get the longest length.
        for j in range(len(DataList)):
            if length[i]<len(DataList[j][i]):
                length[i]=len(DataList[j][i])
    for i in range(len(DataList)):
        for j in range(len(DataList[0])):
            print(DataList[i][j].ljust(length[j]),end='   ')        #Print using ljust, filling with spaces; 3 spaces added to separate the longest rows.
        print()                                                     #equals to '\n'; twice line-changes if use print('\n').


#Function to print log to user; passwords for other users are shown as'******'.
def VisitLog(filepath,UserName):                            #Get the specific user, and only print out that password.
    DataList=numpy.array(ReadLog(filepath))    
    col=len(DataList[0])
    index=FindUser(filepath,UserName)                       #Locate the entry of the user.
    for i in range(len(DataList[0])):                       #Locate the "Password" column.
        if DataList[0][i]=='Password':
            PwdCol=i
    Pwd=DataList[index,PwdCol]                              #Save the password for user in this function.
    for i in range(1,len(DataList)):                        #Mask all password with "******", including this user (that's why I use Pwd to save).
        DataList[i,PwdCol]='******'
    DataList[index,PwdCol]=Pwd                              #Recover the password for the specific user.
    length=[]
    for i in range(col):                                    #Prints out the data using ljust; same as the part in PrintLog function.
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
    Password=DataList[index][PwdCol]            #Extract password of the user.
    Record=DataList[index][RecCol]              #Extract the record of the user (typically '3').
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
                print("Please login anther time.")                          #Lets the new user login at another time.
                return
            else:
                print("Username not exist. Please try another time!")       #For ones don't want to register: quit.
                return
        UserName=input("Username not exist; please re-enter username.\nUsername:")
    index=FindUser(filepath,UserName)       #Track position of the username in file.
    DataList=ReadLog(filepath)
    for i in range(len(DataList[0])):       #Extract the password and record; the record tells how many times this user has failed logging in.
        if DataList[0][i]=='Password':
            PwdCol=i
        elif DataList[0][i]=='Record':
            RecCol=i
    Counter=int(DataList[index][RecCol])    #Check and record failed logins; not yet written into file. Note: data are in str type in list, so int() is used.
    if Counter>2:                           #Check if the user has been blocked by failing logging in 3 times - now blacklist seems to be useless.
        print("Sorry! Your account has been locked!")   #If yes, then pop up warning msg and quit.
        return 0
    Password=input("Password:")             #Input password - the type-in is shown on screen.
    while Password!=DataList[index][PwdCol]:    #When password is incorrect:
        Counter+=1                              #Record+1
        DataList[index][RecCol]=str(Counter)    #Save the record in list, not yet in file.
        if Counter>2:                           #If failures add up to 3:
            CreateLog(DataList,filepath)        #Write the record in file (re-write the whole file).
            BlackList(filepath,UserName)        #Add user to blacklist.
            print("Sorry! You've tried over 3 times, and your account is locked!")
            return 0
        Password=input("Wrong password! You have "+str(3-Counter)+" times to enter password.\nPassword:")   #Re-type password if not failed over 3 times.
    CreateLog(DataList,filepath)                #Write the record (<3) into the file.
    print("Login succesful!")
    VisitLog(filepath,UserName)                 #Print out the list of the users, password as "******" except for this user, and failure records.


#Write the main function: create a file 'userlog.log' when running this script.
def main():
    if __name__==__main__:
        LogIn('userlog.log')
        
        
