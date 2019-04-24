
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

studentData1 = pd.read_csv('StudentData.csv',encoding = 'ISO-8859-1')

ratesData = pd.read_csv('pertusisRates2010_2015.csv',encoding = 'ISO-8859-1')

infantData = pd.read_csv('InfantData.csv',encoding = 'ISO-8859-1')


# In[7]:


print(studentData1.shape)


# In[8]:


studentData1.head(5)


# In[30]:


#Collecting X and Y
X= studentData1['year'].values
Y= studentData1['nPolio'].values


# In[31]:


# Mean X and Y
mean_x= np.mean(X)
mean_y= np.mean(Y)

#Total Number of Values
m = len(X)

#Using the formula to calculate b1 and b2
numer= 0
denom=0
for i in range(m):
    numer += (X[i] - mean_x) * (Y[i] - mean_y)
    denom += (X[i] - mean_x) **2
b1 = numer/denom
b0 = mean_y - (b1*mean_x)

#Print Coefficients
print("Coefficients:\n", b1,b0)


# In[34]:


#Plotting Values and Regression Line
max_x = np.max(X) + 10
min_x = np.max(X) - 10

#Calculating line values x and y
x = np.linspace(min_x, max_x, 2000)
y = b0 + b1 * x

#Ploting Line
plt.plot(X,Y, color='blue', label='Regression Line')

#Ploting Scatter Points
plt.scatter(X, Y, c='green', label='Scatter Plot')

plt.xlabel('year')
plt.ylabel('nPolio')
plt.legend()
plt.show()

