import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# #cleans data
# #Loads the data using pandas
studentData = pd.read_csv('StudentData.csv',encoding = 'ISO-8859-1')

ratesData = pd.read_csv('pertusisRates2010_2015.csv',encoding = 'ISO-8859-1')

infantData = pd.read_csv('InfantData.csv',encoding = 'ISO-8859-1')

# # # Data Cleaning # # # 
# dstudentData = studentData.drop(['SCHOOL','school_code'],axis = 1)
#
# #drop years 2000-2010 and 2015
# for i in range(2000,2010):
#     studentData = studentData[studentData.year != i]
#
# studentData = studentData[studentData.year != 2015]
#
# #sort csv by county
# studentData.sort_values(by=['COUNTY','year'], inplace=True)
#
# #total per county
# data3 = studentData.groupby(['COUNTY','year']).sum()
# #print(data3)
# # saves data to csv
# # added pertussis cases manually
# data3.to_csv (r'combinedDataPairplot.csv')

# csv file that combines studentdata and pertussis rates
dataf = pd.read_csv("final_data.csv",encoding='ISO-8859-1')
for col in dataf.columns:
    if 'Unnamed' in col:
        del dataf[col]

# The pairs plot builds on two basic figures, the histogram and the scatter plot. The histogram on the diagonal allows
# us to see the distribution of a single variable while the scatter plots on the upper and lower triangles show the 
# relationship (or lack thereof) between two variables.
def pairplots():
    sns.pairplot(studentData)
    plt.savefig('studentData_pairplot.png')

    sns.pairplot(dataf)
    plt.savefig('combinedDataPairplot.png')
    
def heatmap():
    corr = dataf.corr()#dataf.loc[:,dataf.dtypes == 'float64'].]corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, cmap=sns.diverging_palette(220, 10, as_cmap=True))
    plt.savefig('heatmap.png')
    
def boxplots():
    sns.boxplot(x=studentData['schoolType'], y=studentData['Avg_nPBE'])
    #plt.show()

def scatterplots():
    #One scatter plot per year
    plt.scatter(dataf['avg_PBE'], dataf['avg_DTP'], color='b')
    plt.xlabel('Average Number of students with Personel Belief Exemption')
    plt.ylabel('Average Number of students with DTap Vaccine')
    plt.savefig('avg_nDTP_nPBE.png')
   
    plt.scatter(dataf['cases'], dataf['nDTP'])#, s=100, c=dataf['year'], cmap=jet)
    plt.savefig('nDTP_nPME.png')
    plt.xlabel('cases')
    plt.ylabel('Number of students with DTap Vaccine')
    
    plt.scatter(dataf['nPME'], dataf['nPBE'], color='b')
    plt.savefig('nPME_nPBE.png')
    plt.xlabel('Number of students with Personel Belief Exemption')
    plt.ylabel('Number of students with DTap Vaccine')
   
def barcharts():
    plt.bar(studentData['year'],studentData['nDTP'])
    #plt.title('My title')
    plt.xlabel('year')
    plt.ylabel('Number of students with DTap Vaccine')
    #plt.show()
    plt.savefig('nDTP_year.png')

    data = studentData.groupby(['schoolType']).sum()
    print(data)
    lst = ['Private', 'Public']
    plt.bar(lst,data['nDTP']/data['n'])
    #plt.title('My title')
    plt.xlabel('School Type')
    plt.ylabel('Number of students with DTap Vaccine')
    #plt.show()
    plt.savefig('nDTP_schoolType.png')

    data = studentData.groupby(['schoolType']).sum()
#    print(data)
    lst = ['Private', 'Public']
    plt.bar(lst,data['nPBE']/data['n'])
    #plt.title('My title')
    plt.xlabel('School Type')
    plt.ylabel('Number of students with Personal Belief Exemption')
    #plt.show()
    plt.savefig('nPBE_schoolType.png')

    data = studentData.groupby(['COUNTY']).sum()
    #print(data)
    lst = list(set(dataf.COUNTY))
    plt.figure(figsize=(20, 20))
    plt.bar(lst,data['nDTP']/data['n'])
    #plt.title('My title')
    plt.xlabel('County', fontsize=22)
    plt.xticks(rotation=75)
    plt.ylabel('Number of students with DTap Vaccine', fontsize=22)
    #plt.show()
    plt.savefig('nDTP_county2.png')

    plt.figure(figsize=(20, 20))
    plt.bar(dataf['COUNTY'],dataf['rates'])
    #plt.title('My title')
    plt.xlabel('County', fontsize=22)
    plt.xticks(rotation=75)
    #fix x tick labels
    plt.ylabel('Rate of Pertussis cases', fontsize=22)
    #plt.show()
    plt.savefig('rates_county.png')

    plt.bar(dataf['year'],dataf['nPBE'])
    #plt.title('My title')
    plt.xlabel('year')
    plt.ylabel('Number of students with personal belief exemption')
    plt.savefig('nPBE_year.png')

    plt.bar(dataf['year'],dataf['cases'])
    #plt.title('My title')
    plt.xlabel('year')
    plt.ylabel('Number of Pertussis Cases')
    plt.savefig('cases_year.png')



pairplots
heatmap()
boxplots()
barcharts()
scatterplots()

