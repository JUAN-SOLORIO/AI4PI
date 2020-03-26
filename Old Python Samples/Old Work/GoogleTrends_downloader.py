#####################################################################################
#       Here we are setting up the libraries that contain the formulas/functions we will use
#       in this program to download and format the Google Trends.
##################################################################################### 

from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import datetime
import os, os.path
import time

date = datetime.datetime.now()
now = date.strftime("%Y%m%d")

#####################################################################################
#       Here we are setting the folder where the code and excel files are located
#       MAKE SURE THE 'infile' DOES NOT GET MOVED FROM THE 'directory' FOLDER. 
#       The 'infile' is necessary because it contains the list of terms for google to look up
#####################################################################################

#file path to googletrens files
directory = '//JB-SAC-FS01/Sources/Predictive-Analytics/GoogleTrends/GoogleDownloaders/'
infile = 'GoogleTrendsTerms.csv'
outfile = 'Google_Metro_Inputs_'+ now +".csv"
oldpath = os.path.join(directory,infile)
newpath = os.path.join(directory,outfile)

#Pandas data frames
pytrend = TrendReq()
load_df = pd.read_csv(oldpath)
df = pd.DataFrame()

#list loading terms from GoogleTrendsTerms.csv
terms_load = []
gmetrocodes_load = []
marketnames_load = []
categories_load = []
estateterms_load = []

df_loaded = load_df.dropna(how='all')     #drop rows containing only 'nan' from the loaded values


for index, row in df_loaded.iterrows():   
    terms_load.append(row['US_TERM'])
    gmetrocodes_load.append(row['MetrosCode'])
    categories_load.append(row['CAT'])
    marketnames_load.append(row['Market'])
    estateterms_load.append(row['TERM'])
    
    
#clean "nan" values from lists
terms = [x for x in terms_load if str(x) != 'nan']
gmetrocodes = [x for x in gmetrocodes_load if str(x) != 'nan']
marketnames = [x for x in marketnames_load if str(x) != 'nan']
category = [x for x in categories_load if str(x) != 'nan']
categories = [int(round(n,0)) for n in category]
estateterms = [x for x in estateterms_load if str(x) != 'nan']

#list for the all the google parameters
GT_trends_all = []
GT_trends_RE = []
GT_trends_listings = []

i = 0

#creating the list of tuples combining the market names and google metro-codes
codes = []
for j in range(max((len(gmetrocodes),len(marketnames)))):
    while True:
        try:
            index_code = (gmetrocodes[j],marketnames[j])
        except IndexError:
            if len(gmetrocodes)>len(marketnames):
                marketnames.append('')
                index_code = (gmetrocodes[j],marketnames[j])
            elif len(gmetrocodes)<len(marketnames):
                gmetrocodes.append('')
                index_code = (gmetrocodes[j],marketnames[j])
            continue
        codes.append(index_code)
        break


#filling the list with the geographic location, google category, and terms
for code in codes:
    #splitting the geographic locations
    if code[0] == 'US':
        for term in terms:
            GT_trends_all.append([categories[0], code[0], code[1], term])
    else:
        for incat in categories:
            if incat == 0:
                for term in estateterms:
                    GT_trends_all.append([incat, code[0], code[1], term])
            else:
                GT_trends_all.append([incat, code[0],code[1], ""])

    #print(code)


print('\n\n\n\n')

#####################################################################################
#       This section is now going into the Google Trends site and pulling 
#       each one of the terms from the lists of trends and metros
#####################################################################################

#pulling trends data from Google trends
for trend in GT_trends_all:
    i += 1
    pytrend.build_payload(kw_list=[trend[3]], cat = trend[0] , geo= trend[1] , timeframe='all')
    
    interest_over_time_df = pytrend.interest_over_time()
    GT_header = "%s-%s-%s"%(trend[2],trend[0],trend[3])
    df[GT_header] = interest_over_time_df[trend[3]]
    print(GT_header)
    if (i==len(GT_trends_all)/4 or i==len(GT_trends_all)/2):
        print("\n Timer Break... Please wait...")
        time.sleep(25)
        


#####################################################################################
#       This section is printing the google trends tables 
#       into individual sheets of an excel file
#####################################################################################
#printing data to the csv file
print('done')    
df.to_csv(newpath)