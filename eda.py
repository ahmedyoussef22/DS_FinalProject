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
    plt.show()

def scatterplots():
    #One scatter plot per year
    # plt.scatter(dataf['avg_PBE'], dataf['avg_DTP'], color='b')
 #    jet=plt.get_cmap('jet')
 #    #plt.scatter(dataf['cases'], dataf['nDTP'], s=100, c=dataf['year'], cmap=jet)
 #    plt.savefig('nDTP_nPME.png')
    
    plt.scatter(dataf['rates'], dataf['avg_PBE'], color='b')
    plt.savefig('rates_nPBE.png')
   
def barcharts():
    # plt.bar(studentData['year'],studentData['nDTP'])
 #    #plt.title('My title')
 #    plt.xlabel('year')
 #    plt.ylabel('Number of students with DTap Vaccine')
 #    #plt.show()
 #    plt.savefig('nDTP_year.png')
 # #
    plt.bar(studentData['schoolType'],studentData['nDTP'])
    #plt.title('My title')
    plt.xlabel('school type')
    plt.ylabel('Number of students with DTap Vaccine')
    #plt.show()
    plt.savefig('nDTP_schoolType.png')

    plt.bar(studentData['COUNTY'],studentData['nDTP'])
    #plt.title('My title')
    plt.xlabel('county')
    plt.ylabel('Number of students with DTap Vaccine')
    #plt.show()
    plt.savefig('nDTP_county.png')

    plt.bar(dataf['COUNTY'],dataf['rates'])
    #plt.title('My title')
    plt.xlabel('county')
    #fix x tick labels
    plt.ylabel('Percent of Pertussis cases')
    #plt.show()
    plt.savefig('avg_cases_county.png')
  #
    plt.bar(studentData['schoolType'],studentData['nPBE'])
    #plt.title('My title')
    plt.xlabel('school type')
    plt.ylabel('Number of students with personal belief exemption')
    #plt.show()
    plt.savefig('nPBE_schoolType.png')
 
    plt.bar(dataf['year'],dataf['PBE'])
    #plt.title('My title')
    plt.xlabel('year')
    plt.ylabel('Number of students with personal belief exemption')
    plt.savefig('nPBE_year.png')

    
#pairplots  
#heatmap()
#boxplots()  
barcharts()
#scatterplots()
