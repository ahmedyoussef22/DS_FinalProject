# import: numpy, pandas, and plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from collections import OrderedDict
from sklearn.metrics import accuracy_score
# all the data
studentData = pd.read_csv('StudentData.csv',encoding = 'ISO-8859-1')
ratesData = pd.read_csv('pertusisRates2010_2015.csv',encoding = 'ISO-8859-1')
# observing student data we need to drop data on nMMR and nPolio since we are interested only in Pertussis outbreaks
# also, we need to drop data on 2015 year as well as years 2000-2009 since we are only interested in 2010-2014 years
# lastly, we need to sort the data's rows according to years and county from lowest to highest
studentData = studentData.drop(['schoolType','SCHOOL','school_code','nMMR', 'nPolio'], axis=1)
for i in range(2000,2010):
    studentData = studentData[studentData.year != i]
studentData = studentData[studentData.year != 2015]
studentData = studentData.sort_values(by=['COUNTY', 'year'])
# on rates data we will drop first row as it contains cases for entire California
ratesData = ratesData.iloc[1:]
# now we calculate the not vaccinated number of students for all counties
studentData['not_vaccinated'] = studentData['n'] - studentData['nDTP']
# create the data frame
cols = ['county','students','vaccinated','not_vaccinated','belief_exemptions','medical_exemptions','year','cases']
df = pd.DataFrame( columns = cols)
yrs = [2010,2011,2012,2013,2014]
for x in yrs:
    new_df = studentData[studentData['year']==x]
    for i in sorted(set(new_df['COUNTY'].tolist())):
        new_df2 = new_df[new_df['COUNTY']==i]
        df = df.append({'county' : i , 
                        'students' : new_df2['n'].sum() ,
                        'vaccinated' : new_df2['nDTP'].sum() ,
                        'not_vaccinated' : new_df2['not_vaccinated'].sum() ,
                        'belief_exemptions' : new_df2['nPBE'].sum() ,
                        'medical_exemptions' : new_df2['nPME'].sum() ,
                        'year' : x
                       } ,ignore_index=True)
        
df = df.sort_values(by=['county', 'year'])
# to account for missing ALPINE county for 2014 year
df = df.append({'county' : 'ALPINE' , 'students' : 0, 'vaccinated' : 0, 'not_vaccinated' : 0, 'belief_exemptions' : 0, 'medical_exemptions' : 0, 
               'year' : 2014, 'cases' : 0 } , ignore_index=True)
df = df.sort_values(by=['county', 'year'])

vaccinated_2014 = []
not_vaccinated_2014 = []
for i in range(len(df['year'])):
    if df['year'].tolist()[i] == 2014:
        vaccinated_2014.append(df['vaccinated'].tolist()[i])
        not_vaccinated_2014.append(df['not_vaccinated'].tolist()[i]) 
# now we drop data for 2014 as we do not need it from here
df = df[df.year != 2014]

rates_new = ratesData.drop(['Rate2010','Rate2011','Rate2012', 'Rate2013','Rate2014','Cases2014'], axis=1)
conv = rates_new.T
l = []
for i in conv:
    for w in range(1,len(conv[i].tolist())):
        l.append(conv[i].tolist()[w])  
df['cases'] = l
# variables used for averages calculation
a = 0
b = 0
c = 0
d = 0

e = 0
f = 0
g = 0
h = 0

u = 0
t = 0
y = 0
o = 0

res1 = 0
res2 = 0
res3 = 0
counties = []
avg_cases = []
avg_vacc = []
avg_notVacc = []
# loop through and calculate the averages
for i in range(0, len(df['cases']), 4):
    counties.append(df['county'].tolist()[i])
    
    a = df['vaccinated'].tolist()[i]
    b = df['vaccinated'].tolist()[i+1]
    c = df['vaccinated'].tolist()[i+2]
    d = df['vaccinated'].tolist()[i+3]
    
    e = df['not_vaccinated'].tolist()[i]
    f = df['not_vaccinated'].tolist()[i+1]
    g = df['not_vaccinated'].tolist()[i+2]
    h = df['not_vaccinated'].tolist()[i+3]
    
    u = df['cases'].tolist()[i]
    t = df['cases'].tolist()[i+1]
    y = df['cases'].tolist()[i+2]
    o = df['cases'].tolist()[i+3]
    
    res1 = round((a+b+c+d)/4)
    res2 = round((e+f+g+h)/4)
    res3 = round((u+t+y+o)/4)
    
    avg_vacc.append(res1)  
    avg_notVacc.append(res2)
    avg_cases.append(res3)
cols = ['vaccinated_avg','not_vaccinated_avg','cases_avg']
final_df = pd.DataFrame( columns = cols)
final_df['vaccinated_avg'] = avg_vacc
final_df['not_vaccinated_avg'] = avg_notVacc
final_df['cases_avg'] = avg_cases
cols = ['vaccinated','not_vaccinated']
data_2014 = pd.DataFrame( columns = cols)
data_2014['vaccinated'] = vaccinated_2014 
data_2014['not_vaccinated'] = not_vaccinated_2014
# scale the data

standardScaler = StandardScaler()
scale_these = ['vaccinated_avg', 'not_vaccinated_avg', 'cases_avg']
final_df[scale_these] = standardScaler.fit_transform(final_df[scale_these])
# use a 70 to 30 training to testing split

Y = final_df['cases_avg']
X = final_df.drop(['cases_avg'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=0)
# fit the data into the model

regressor = LinearRegression()
regressor.fit(X_train, y_train)
predection_list = regressor.predict(data_2014)
predection_list = [round(x) for x in predection_list]

d = dict((el,0) for el in counties)
index = 0
for i in d:
    d[i] = predection_list[index]
    index += 1
# calculate the accuracy

d_descending = dict(OrderedDict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)))
# sort rates data according to year 2014 from highest cases to lowest cases in all counties
ratesData = ratesData.sort_values(by=['Cases2014'],ascending=False)
pred = list(d_descending.keys())
acc = accuracy_score(ratesData['county'].tolist(), pred)
print("Accuracy:",acc*100, "%")

# highest risk: LOS ANGELES
# second highest risk: SAN DIEGO
# comparing to actual cases of 2014, the last 6 counties of 2014 had values of 0 cases
print("Actual VS. Predicted")
for i in range(len(pred)):
    print(ratesData['county'].tolist()[i], " VS. ",pred[i])