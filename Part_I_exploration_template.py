#!/usr/bin/env python
# coding: utf-8

# # Ford GoBike System Data
# ## by (Oyinkansola Oshikoya)
# 
# ## Introduction
# 
# The dataset consist of records about bike trips made by individuals in the Ford GoBike System bike-sharing system in San Francisco Bay area in February 2019.
# 
# 
# ## Preliminary Wrangling
# 

# In[1]:


# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Dataset is being loaded to a dataframe
df_bike=pd.read_csv('201902-fordgobike-tripdata.csv')


# In[3]:


# Dataset is being inspected
df_bike.head()


# In[4]:


# Viewing the various measures and aggregation
df_bike.describe()


# In[5]:


# Viewing the dataset structure
df_bike.shape


# In[6]:


# Viewing the dataset properties

df_bike.info()


# In[7]:


# Checking for null values
df_bike.isnull().sum()


# In[8]:


# Checking for duplicated values
df_bike.duplicated().sum()


# In[9]:



# Dropping all null values
df_bike.dropna(inplace=True)


# In[10]:


# Checking for null values
df_bike.isnull().sum()


# In[11]:


# Dropping the "station_id" and "end_station_id" columns.

df_bike.drop(['start_station_id', 'end_station_id'], axis=1, inplace=True)


# In[12]:


# Converting the data type of "start_time" from object to datetime.
df_bike['start_time']= pd.to_datetime(df_bike['start_time'])


# In[13]:


# Creating a new column to create year.
df_bike['start_year']=df_bike['start_time'].dt.year


# In[14]:


# Creating a new column for "start_day_of_week", which converts the "start_time" to days.

df_bike['start_day_of_week']=df_bike['start_time'].dt.day_name()


# In[15]:


# Creating a new column for "start_hour_of_day", which converts the "start_time" to hours.

df_bike['start_hour_of_day']=df_bike['start_time'].dt.hour


# In[16]:


# Converting the birth year to integer.
df_bike['member_birth_year']=df_bike['member_birth_year'].astype(int)


# In[17]:


# Calculating the age.
df_bike['age']=df_bike['start_year'] - df_bike['member_birth_year']


# In[18]:


# Converting the data type of "end_time" from object to datetime.
df_bike['end_time']= pd.to_datetime(df_bike['end_time'])


# In[19]:


# Creating a new column for "end_day_of_week", which converts the "end_time" to days.
df_bike['end_day_of_week']=df_bike['end_time'].dt.day_name()


# In[20]:


# Creating a new column for "end_hour_of_day", which converts the "end_time" to hours.
df_bike['end_hour_of_day']=df_bike['end_time'].dt.hour


# In[21]:


# Converting from seconds to minutes.
df_bike['duration_min'] = df_bike['duration_sec']/60


# In[22]:



# Converting "duration_min" to integer.
df_bike['duration_min'] = df_bike['duration_min'].astype(int)


# In[23]:


# Deleting the "duration_sec" column since the "duration_min" will be used.
df_bike.drop(columns=['duration_sec'], inplace=True)


# In[24]:


# Renaming the columns of 'bike_share_for_all_trip' to a short name.
df_bike.rename(columns = {'bike_share_for_all_trip':'bike sharing'}, inplace = True)


# In[25]:


# Importing math lab to calculate distance base on latitude and longitude.
import math
from math import radians, sin, cos, acos
def distancekm(origin, destination):
    latitude1, longitude1 = origin
    latitude2, longitude2 = destination
    radius = 6371 # this is in kms
    dlat = math.radians(latitude2 - latitude1)
    dlong = math.radians(longitude2 - longitude1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(latitude1)) 
         * math.cos(math.radians(latitude2)) * math.sin(dlong / 2) * math.sin(dlong / 2))
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    c = radius * b
    return c


# In[26]:


# creating the column 'distance_km'.
   
df_bike['distance_km'] = df_bike.apply(lambda x: distancekm((x['start_station_latitude'], x['start_station_longitude']), (x['end_station_latitude'], x['end_station_longitude'])), axis=1)


# In[27]:


# Converting the column 'distance_km' to integer.
df_bike['distance_km'] = df_bike['distance_km'].astype(int)


# In[28]:


# Inspecting the data structure for changes implemented
df_bike.info()


# In[29]:


# Inspecting the data structure
df_bike.head()


# In[30]:


# Inspecting the data structure
df_bike.shape


# In[31]:


df_bike.to_csv('fordgobike_cleaned.csv', index = False)


# ### What is the structure of your dataset?
# 
# > There are 174,952 records with 20 different attributes such as duration_sec, start_time, end_time, start_station_name, start_station_latitude, start_station_longitude, end_station_name, end_station_latitude, end_station_longitude, bike_id, user_type, member_birth_year, member_gender, bike_share_for_all_trip, start_month, start_day_of_week, start_hour_of_day and end_month after data cleanup was implemented.
# 
# 
# 
# ### What is/are the main feature(s) of interest in your dataset?
# 
# > I am interested in detecting the number of trips,duration spent and distance covered based on user type, gender, bike sharing, age, start days and end days.
# 
# ### What features in the dataset do you think will help support your investigation into your feature(s) of interest?
# > The count of the different categories based on the user type, gender, bike sharing, start days and end days.
# > The trip duration based on the user type, gender, bike sharing and start days.

# ## Univariate Exploration

# In[32]:


# Creating a function for repetitive labels.
def titlelabels(title,xlabel,ylabel):
       plt.title(title, fontsize=16, fontweight='bold')
       plt.xlabel(xlabel)
       plt.ylabel(ylabel)
       
       
       


# > What Start day of the week has the highest number of trips?

# In[33]:


# This gives the total number of trips that occurred on various start days of the week. 
plt.figure(figsize = [10, 8])
base_color = sb.color_palette()[0]
base_order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
sb.countplot(data=df_bike, x='start_day_of_week', color=base_color, order=base_order)
titlelabels('TOTAL NUMBER OF TRIPS ON VARIOUS START DAYS','NUMBER OF TRIP', 'START DAY OF WEEK');


# > Thursdays have the highest number of trips while the weekends has the lowest values.

# > Do the end and start day of the week have the same number of trips?

# In[34]:


# Checking if trips ended in subsequent days
plt.figure(figsize = [10, 8])
sb.countplot(data=df_bike, x='end_day_of_week', color=base_color, order=base_order)
titlelabels('TOTAL NUMBER OF TRIPS ON VARIOUS END DAYS','NUMBER OF TRIPS', 'END DAY OF THE WEEK');


# > The number of trips for the start and end day of the week are the same. This implies that all trips began and ended in the same day.

# > What hour of the day has the highest number of trips?

# In[35]:


# Checking to detect the peak hours when bikes are ridden
plt.figure(figsize = [10, 8])
sb.countplot(data=df_bike, x='start_hour_of_day', color=base_color)
titlelabels('NUMBER OF TRIPS AT VARIOUS START HOURS', 'START HOUR OF THE DAY', 'NUMBER OF TRIPS');


# > The peak hours are 8 and 17. This signifies that bikes are often ridden majorly at the start and close time of working hours.

# > What category of the user type has the highest number of trips?

# In[36]:


# Checking to detect the highest number of trips based on user tpe.
plt.figure(figsize = [12, 8])
sorted_counts = df_bike['user_type'].value_counts()
plt.pie(sorted_counts, labels = sorted_counts.index, startangle = 90, counterclock = False)
plt.axis('square')
plt.title('THE TOTAL NUMBER OF TRIPS BASED ON USER TYPE', fontsize=16, fontweight='bold');


# > The plot above shows that majority of individuals are subscribers, which might be cost effective for them.

# > What gender has the highest number of trips?

# In[37]:


# Checking to discover the gender with the highest number of trips
sorted_counts = df_bike['member_gender'].value_counts()
plt.figure(figsize = [12, 8])
plt.pie(sorted_counts, labels = sorted_counts.index, startangle = 90, counterclock = False)
white_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(white_circle)
plt.title('THE TOTAL NUMBER OF BIKE USERS BASED ON GENDER', fontsize=16, fontweight = 'bold')
plt.axis('square')
plt.show()


# > The plot shows that majority of the bike riders are male. Fordbike can shows adverts to more men to increases its number of customers or subscribers.

# > Are bikes often shared for the trips?

# In[38]:


plt.figure(figsize = [11, 8])

sb.countplot(data=df_bike, x='bike sharing',color=base_color)
titlelabels('TOTAL NUMBER OF TRIPS BASED ON BIKE SHARING','BIKE SHARING STATUS', 'NUMBER OF TRIPS');


# > The plot shows that majority do not share bikes for trips.

# What are the top 10 ages with the highest number of trips?

# In[39]:


# Checking to detect the age with the highest number of trips

plt.figure(figsize = [11, 8])
agecategorisation=df_bike['age'].value_counts()
agecategorisation[:10].plot(kind='bar', color=base_color)
titlelabels("TOP 10 AGES WITH THE HIGHEST NUMBER OF TRIPS", "age", "number of trips");


# The graph shows that those who are 31 years old often have the highest number of trips

# ### Discuss the distribution(s) of your variable(s) of interest. Were there any unusual points? Did you need to perform any transformations?
# 
# > There was no unusual distribution. 
# <br>A transformation was done to convert the "duration_sec" to duration in minutes, and it was converted to integer for easy analytics.
# <br> A new column "distance_km" was created to get the distance covered.
# <br> A new column "age" was derived.
# 
# ### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?
# 
# > There was no unusual distributions.

# ## Bivariate Exploration
# 
# 

# > What category of user type had a higher trip duration?

# In[40]:


# Checking the relationship between the trip durarion and user type

plt.figure(figsize = [10, 8])
sb.boxplot(data = df_bike, x = 'user_type', y = 'duration_min', color=base_color)
titlelabels('CUSTOMERS VS SUBSCRIBERS TIME DURATION ON TRIP', 'USER TYPE', 'DURATION IN MINUTES')
plt.show()


# > The plot shows that customers spend more duration on trips than subcribers as seen in previous graph. This implies that being a subscriber has the benefit of having a lesser trip duration.

# > What category of user type has a higher number of bike sharing for the trips?

# In[41]:


# Checking what user type had the higher number of bike sharing 
plt.figure(figsize = [12, 8])
sb.countplot(data = df_bike, x = 'user_type', hue='bike sharing')
titlelabels('NUMBER OF TRIPS BASED ON USER TYPE AND BIKE SHARING', 'user type', 'NUMBER OF TRIPS')
plt.show();


# > The graph shows that subscribers have access to  bike sharing sharing because there is none attached to customers.

# > What category of user had the higher distance covered?

# In[42]:


# Investigating the distance covered by user type.
plt.figure(figsize = [10, 8])
sb.boxplot(data = df_bike, x = 'user_type', y = 'distance_km', color=base_color)
titlelabels('CUSTOMERS VS SUBSCRIBERS DISTANCE COVERED ON TRIP', 'USER TYPE', 'DISTANCE COVERED(KM)')
plt.show();


# > The graph shows that customers have the higher distance covered.

# > What gender often share bikes for the trips?

# In[43]:


# Checking the number of trips by the gender type based on bike sharing.
plt.figure(figsize = [12, 8])
sb.countplot(data = df_bike, x = 'member_gender', hue = 'bike sharing')
titlelabels('NUMBER OF TRIPS BASED ON BIKE SHARING BY GENDER', 'gender', 'NUMBER OF TRIPS')
plt.show();


# > The plot shows that the male gender has the highest number of trips and bike sharing.

# > What day of the week has the highest number of bike sharing?

# In[44]:


# Investigating what day of the week has the highest number of bike sharing .
plt.figure(figsize=(10,6))
sb.countplot(data=df_bike, x='end_day_of_week',  order=base_order, hue='bike sharing');
titlelabels('THE NUMBER OF TRIPS BASED ON BIKE SHARING ON WEEK DAY', 'week day' , 'number of trips')
plt.show();


# > The graph show that the highest number of trips and bike sharing occurs on Thursday as seen in the univariate visualisation because it is a peak period.

# ### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?
# 
# #### The following trends were observed in the univariate and bivariate
# > The highest number of trips occurs on Thurdays.
# <br> Subscribers have the higher number of trips.
# <br> The highest number of trips are often by males.
# <br> Trip duration is higher for customers than subscribers
# <br> Trip often begins and end on the same day.
# <br> Customers often have higher distances covered.
# 
# 
# 
# 
# ### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?
# 
# > Majority of the bike riders are subscribers
# <br> The peak period occurs on Thursdays
# <br> The highest number of bike sharing occurs on Thursdays.
# <br> The majority of the riders are male.
# <br> Customers have a higher trip duration and distance covered than subscribers. 
# <br> Customers do not have the benefit of bike sharing.
# <br> Bikes are often not shared for trips.
# <br> Males often share bikes
# 

# ## Multivariate Exploration
# 

# > What gender in the user category had the highest number of trip duration?

# In[45]:


plt.figure(figsize=(10,6))
g = sb.FacetGrid(data = df_bike, col = 'user_type')
g.map(sb.boxplot, 'member_gender', 'duration_min');


# > Plot shows that male in the subsciber category had the highest duration trip, and the other gender in the customer category had the highest duration trip.

# > What day of the week had the long distance covered with the highest bike sharing? 

# In[46]:


# Checking to discover the day of the week,which had the longest distance with the highest bike sharing.
plt.figure(figsize=(10,6))

sb.barplot(data=df_bike, x='start_day_of_week', y='distance_km', order=base_order, hue='bike sharing', ci=None)

titlelabels('DISTANCE COVERED BASED ON BIKE SHARING FOR THE DAY OF THE WEEK','day of the week', 'distance covered')


# > The plot shows that Thursdays often have the highest distance covered with the highest bike sharing. 

# > What plot has the highest number of bike sharing?

# In[47]:


plt.figure(figsize=(10,6))
g = sb.FacetGrid(data = df_bike, col = 'member_gender')
g.map(sb.boxplot, 'bike sharing', 'duration_min');


# >The graph shows that maleo ften share bikes

# > What day of the week has the highest number of trip duration?

# In[48]:


plt.figure(figsize=(10,6))
titlelabels('TRIP DURATION BASED ON GENDER FOR WEEK DAY', 'day of the week', 'distance duration_min')
sb.barplot(data=df_bike, x='start_day_of_week', y='duration_min', order=base_order, hue='member_gender', ci=None);


# > The other gender has the highest number of duration on week days.

# > What  user type has the highest trip distance covered and biking on days of the week?

# In[49]:


plt.figure(figsize=(10,6))
titlelabels('DISTANCE COVERED BASED ON USER TYPE FOR WEEK DAY', 'day of the week', 'distance covered')
sb.barplot(data=df_bike, x='start_day_of_week', y='distance_km', order=base_order, hue='user_type', ci=None);



# The plot shows that customers have the large distance covered and bike sharing.

# ### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?
# 
# > Implementing more analytics on the trip duration showed that customers often have higher trip duration.
# > The other gender has the highest duration trip.
# 
# 
# ### Were there any interesting or surprising interactions between features?
# 
# > There was no interesting interactions between features.

# ## Conclusions
# > Based on the explorations carried out, it is better to be a subscriber because there is access to bike sharing, lower distance covered and low trip duration.
# 

# Reference: MaryamOsamaX, Ford-GoBike-System-Data-Visualization/exploration.ipynb,  Jan 6, 2021
