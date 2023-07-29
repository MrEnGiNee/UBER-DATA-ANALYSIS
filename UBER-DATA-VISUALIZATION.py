#!/usr/bin/env python
# coding: utf-8

# # UBER DATA VISUALIZATION

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Load the dataset

uber = pd.read_csv('C:/Users/dell/Downloads/UBER/uber-raw-data.csv')


# In[4]:


# Display the head of the dataset

uber.head()


# In[5]:


uber.info()


# In[6]:


# Check if there is any missing values

def num_missing(x):
    return sum(x.isnull())
print('Number of missing/null values per column')
print(uber.apply(num_missing, axis=0))


# In[7]:


uber.isnull().sum()


# In[27]:


# Extract additional information
uber['Date/Time'] = pd.to_datetime(uber['Date/Time'], format="%m/%d/%Y %H:%M:%S")
uber['DayofWeekNum'] = uber['Date/Time'].dt.dayofweek
uber['DayofWeek'] = uber['Date/Time'].dt.day_name()
uber['DayNum'] = uber['Date/Time'].dt.day
uber['HourOfDay'] = uber['Date/Time'].dt.hour


# In[28]:


# Display the head of the dataset
uber.head()


# In[29]:


# Display the shape
uber.shape


# In[30]:


# Unique base codes

uber['Base'].unique()


# In[36]:


# Total rides based on the base code

sns.catplot(x='Base', data=uber, kind='count')


# In[38]:


uber_week_data = uber.pivot_table(index=['DayofWeekNum','DayofWeek'], values='Base', aggfunc='count')
uber_week_data


# In[39]:


# Visualize the pivot table
uber_week_data.plot(kind='bar', figsize=(8,6))


# In[41]:


uber_hourly_data = uber.pivot_table(index=['HourOfDay'], values='Base', aggfunc='count')
uber_hourly_data.plot(kind='line', figsize=(10,6), title='Hourly Journeys')


# In[45]:


uber_day_data = uber.pivot_table(index=['DayNum'], values='Base', aggfunc='count')
uber_day_data.plot(kind='bar', figsize=(10,5), color='r', title='Journeys by DayNum')


# In[46]:


def count_rows(rows):
    return len(rows)

by_date = uber.groupby('DayNum').apply(count_rows)
by_date


# In[47]:


#Sort Day of the month by values rather than date
by_date_sorted = by_date.sort_values()
by_date_sorted


# In[49]:


# Analyze the hours

plt.hist(uber.HourOfDay, bins = 24, range = (.5, 24))


# In[51]:


count_rows(uber)
by_hour_weekday = uber.groupby('HourOfDay DayofWeekNum'.split()).apply(count_rows).unstack()
by_hour_weekday


# In[52]:


# heat map the brightest spot shows the day/hour with the highest frequency
plt.figure(figsize=(15,10))
sns.heatmap(by_hour_weekday)


# In[53]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[56]:


import matplotlib.pyplot as plt

plt.scatter(uber.iloc[:, 2], uber.iloc[:, 1])
plt.show()


# ### UBER LOCATION TRACKER

# In[59]:


import folium
import pandas as pd
uber_datanew = pd.DataFrame(uber)


# uber_data_values
uber_two_column = uber_datanew.loc[0:300, 'Lat':'Lon']

uber_data_values = uber_two_column.values.tolist()
newyork_map = folium.Map(location=[40.79659011772687, -73.87341741832425], zoom_start=13)
for point in range(0, len(uber_data_values)):
    folium.Marker(uber_data_values[point], popup=uber_data_values[point]).add_to(newyork_map)

newyork_map

