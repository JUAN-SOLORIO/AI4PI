import numpy as np
import pandas as pd
from datetime import datetime


# Using only numpy and pandas for minimal data frame and 
# reading data from and to file. 
#--------------------------------------------------------

def prepare_data(df_in):
    # function to prepare the dataframe. Takes in dataframe
    # check it has necessary columns, combines latitute and longitude
    # as strings to form location column
    # returns data frame of only userId and Location
    
    checkinputs = ['userId','latitude','longitude'] # columns that must exist in df
    names = df_in.columns # all column names in df
    
    # cheking if data frame is empty or is missing column names
    if len(names)==0:
        if len(df_in)==0:
            print("data frame is empty")
        else:
            print("df does not have header titles")
    else:
        n = 0 # counter to check all 3 variables are in the data frame columns 
        for checkinput in checkinputs:
            if checkinput in names:
                n = n + 1
                next
            else:
                print("The data is missing " + checkinput + " input, or column name " + checkinput +" not found")
    if n==3 :
        df1 = df_in.copy()
        df1['Location'] = df1['latitude'].astype(str) + df1['longitude'].astype(str)
    else:
        print('please fix errors to and rerun')
    return df1[['userId','Location']]


def unique(list1): 
    # function to find all distinct values in a list
    # returns the subset of distincts values from original list
    #-----------------------------------------------
    
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set))
    return unique_list
    
def entropy_fx(my_list): 
    # Function to calculate the probability (frequency) of each userId for given location 
    # returns a list of probabilities for the location
    #------------------------------------------------------------------------
    
    # function maps frequency (p) to -p*log2(p) 
    # for x>0, and to 0 otherwise 
    h = lambda p: -p*np.log2(p) if p > 0 else 0
    
    # setting values for distinct userIds in the location list
    # and for the total number of userIds in the location list
    items = unique(my_list)
    sum_n=len(my_list)
    sum_m=len(items)
    
    # setting an empty list for the probabilities
    prob=[None]*sum_m
    
    # loop to fill prob list with probabilities for each userId
    for count,item in enumerate(items): 
        prob[count] = h(my_list.count(item)/sum_n)  # filling list with Probabilities
    
    return sum(prob)


def entropy_computation(file):
    # function takes in cvs file, converts to pandas dataframe,
    # calls on 'prepare_data' 'unique' and 'entropy_fx' to calculate
    # the entropy of the 'Location' attribute (location = latitute+longitude)
    # outputs a csv file with Location as ID and location-entropy value
    
    df_in = pd.read_csv(file) # opening csv file as pandas df
    location_entropy = [] # initiating an empty list for location entropies
    df1 = prepare_data(df_in) # calling prepare_data to have dataframe with userIds and Locations
    locations = unique(df1['Location']) # list of unique locations in the data to iterate
    
    for i,location in enumerate(locations):
        # loop iterates through locations and fills location entropy
        # by using entropy_fx function
        userlist = list(df1[df1['Location']==location].userId) # unique userIds list
        entro = entropy_fx(userlist) 
        location_entropy.append(entro)

    # ouput to csv file with time stamp
    dateTimeObj = datetime.now() # onject containing time and date
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    
    (pd.DataFrame(list(zip(locations,location_entropy)),columns=['ID','location-entropy'])
        .to_csv('ouput - ' + timestampStr + '.csv'))
