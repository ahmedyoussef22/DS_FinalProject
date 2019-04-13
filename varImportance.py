import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

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

X = dataf.drop("COUNTY", axis = 1)#iris.iloc[:,0:4]
Y = dataf['cases']#iris.iloc[:,-1]
names = dataf.columns.values

# Build the model
rfc = RandomForestClassifier()

# Fit the model
rfc.fit(X, Y)

# Print the results
print("Features sorted by their score:")
print(sorted(zip(map(lambda x: round(x, 4), rfc.feature_importances_), names), reverse=True))

# Isolate feature importances 
importance = rfc.feature_importances_

# Sort the feature importances 
sorted_importances = np.argsort(importance)

# Insert padding
padding = np.arange(len(names)-1) + 0.5

# Plot the data
plt.barh(padding, importance[sorted_importances], align='center')

# Customize the plot
plt.yticks(padding, names[sorted_importances])
plt.xlabel("Relative Importance")
plt.title("Variable Importance")

# Save the plot
plt.savefig('variableImportance.png')