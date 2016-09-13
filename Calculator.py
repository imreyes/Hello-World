# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 15:57:19 2016

@author: GY
"""

#Function groups to mimick a simple calculator. An excercise of Regular Expression.

import re



#Function to clean up the formula; e.g. 2*-4/-3 (=> --2*4/3) => 2*4/3.
def cleanf(formula):
    oprts=re.findall('[\+\-\*\/]{1,2}',formula)             #Get all operators +-*\
    if re.findall('^\d',formula):                           #Ensure the operator position in the beginning; helps simplify the code.
        oprts.insert(0,'+')
    nums=re.findall('[0-9\.\(\)]+',formula)                 #Form data blocks separated by the operators.
    i=0
    for i in range(len(oprts)):
        if len(oprts[i])==1:                                #No redundant operators.
            continue
        elif len(oprts[i])>2:                               #Report error when more than 2 operators in a row.
            print("Error in formula input: inappropriate successive operators")
            return False
            break
        j=i                                                 #Use iterable j in replace of i: j will move backward when iterating.
        while oprts[j][0]=='*' or oprts[j][0]=='/':         #For */ expressions with negative value (e.g. 5*2/-3), move the neg sign stepwise before all */ operators.
            if oprts[j][1]=='+':
                oprts[j]=oprts[j][0]                        #In case there is '*+', remove '+'. Not expected to happen unless input this way.
                continue
            oprts[j-1]+=oprts[j][1]                         #Move the neg sign one step left: (e.g. 5*2/-3 => 5*-2/-3
            oprts[j]=oprts[j][0]                            # 5*-2/-3=> -5*2/3
            j-=1                                            #Repeat when the left operator is also * or /.
        if oprts[j][0]==oprts[j][1]:                        #The basic operator is no longer */, but +-; now simplify it: ++=--=+
            oprts[j]='+'
        else:                                               # +-=-+=-
            oprts[j]='-'
    newform=''                                              #Read the sorted operators back into the newform.
    for i in range(len(oprts)):                             #Read in pairs of operator+expression, as they must come in turn.
        newform+=(oprts[i]+nums[i])
    return newform


#Function to perform */ calculation from string.
def muldiv(formula):
    formula=cleanf(formula)                             #Clean up the expression.
    nums=re.findall('\-?\d*\.\d+|\-?\d+',formula)       #Extract all numbers into a list, including +- signs where applicable.
    oprts=re.findall('[\*\/]',formula)                  #Extract operators '*' and '/'.
    if not oprts:                                       #Return formula if formula is a number.                   
        return float(formula)
    result=float(nums[0])                               #Convert string to float number.  
    for i in range(len(nums)-1):
        if oprts[i]=='*':                               #"Translate" operation from character.
            result*=float(nums[i+1])
        elif oprts[i]=='/':
            if float(nums[i+1])==0:                     #In case number is divided by 0.
                print("Error: number divided by zero")
                return 0
                break
            result/=float(nums[i+1])
        else:                                           #Return error when inappropriate operators are seen - cleanf() should have eliminated intermittant +-.
            print("Error in formula detected: wrong operators other than '*&/'")
            return False
            break
    return result                                       #Return result as float.



#Function to perform +-*/ calculation from string.
def pmpdcal(formula):
    formula=cleanf(formula)
    nums=re.findall('[^\+\-]+',formula)                  #Partition the formula into sections with only */.
    oprts=re.findall('[\+\-]',formula)                   #Extract +- operators.
    if len(oprts)<=1:      
        return muldiv(formula)
    result=0.0                                             #Initiate the sum.
    for i in range(len(nums)):
        if oprts[i]=='+':                                #"Translate" operation from character.                      
            result+=muldiv(nums[i])
        elif oprts[i]=='-':
            result-=muldiv(nums[i])
        else:
            print("Error in formula detected: wrong operators other than '+&-'")        #Return error for wrong operators.
            return False
            break
    return result                                         #Return result as string.





# Function to perform overall calculation.
def calculator(formula):
    formula=cleanf(formula)
    parlist=re.findall('\([^\(\)]+\)',formula)          #Locate all expressions in inner parentheses.
    while parlist:
        for item in parlist:
            pos=formula.find(item)                      #Locate position of each expression.
            length=len(item)                            #Measure length of the expression.
            value=pmpdcal(item[1:-1])                   #Calculate the value.
            formula=formula[:pos]+str(value)+formula[(pos+length):]     #Important part: replace the expression with its value (as string) in the formula, deleting the parentheses.
        formula=cleanf(formula)                         #Cycle the function until no parentheses exist.
        parlist=re.findall('\([^\(\)]+\)',formula)
    return pmpdcal(formula)