from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import datetime
import os, os.path
import time

date = datetime.datetime.now()
now = date.strftime("%Y%m%d")

#file path to googletrens files
directory = '//JB-SAC-FS01/Sources/Predictive-Analytics/GoogleTrends/GoogleDownloaders/'
infile = 'GoogleTrendsTerms_TopMarkets.csv'
outfile = 'Google_Metro_Inputs_RRRA_'+ now +".csv"
path = os.path.join(directory,'Google_Metro_Inputs_RRRA_'+ now +".xlsx")
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
    terms_load.append(row['CAT_TERM'])
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
    if code[0] == 'not a value':
        for term in terms:
            GT_trends_all.append([categories[0], code[0], code[1], term])
    else:
        n = 0
        for incat in categories:
            if incat == 0:
                for term in estateterms:
                    GT_trends_all.append([incat, code[0], code[1], term, term])
            else:
                n += 1
                GT_trends_all.append([incat, code[0],code[1], "", terms[n]])

    #print(code)


print('\n\n\n\n')
print("Downloading...")

#####################################################################################
#       This section is now going into the Google Trends site and pulling 
#       each one of the terms from the lists of trends and metros
#####################################################################################

#pulling trends data from Google trends
for trend in GT_trends_all:
    #print("Downloading...")
    i += 1
    pytrend.build_payload(kw_list=[trend[3]], cat = trend[0] , geo= trend[1] , timeframe='all')
    
    interest_over_time_df = pytrend.interest_over_time()
    GT_header = "%s - %s"%(trend[2],trend[4])
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
print('\n Download done')    
#df.to_csv(newpath)



Remodel_df = df.filter(regex = 'Remodel')
print(Remodel_df.head())
Refinance_df = df.filter(regex = 'Refinance')
Relocation_df = df.filter(regex = 'Relocation')
AptsRes_df = df.filter(regex = 'Apts&Res')
print(AptsRes_df.head())

with pd.ExcelWriter(path, engine = 'xlsxwriter') as writer:
    Remodel_df.to_excel(writer, sheet_name = 'Remodel')
    Refinance_df.to_excel(writer, sheet_name ='Refinance')
    Relocation_df.to_excel(writer, sheet_name ='Relocation')
    AptsRes_df.to_excel(writer, sheet_name ='Apts&Res')


print('File created')
