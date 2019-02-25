#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * The most popular and most profitable item is "Oathbreaker, Last Hope of the Breaking Storm," purchased 12 times and earning a total of $50.76.
# 
# * Users age 35-39 spend more on average than other age groups.
# 
# * User Lisosia93 is the highest spender, purchasing a total of $18.96.
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
purchase_data_csv = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchasedata_df = pd.read_csv(purchase_data_csv)
purchasedata_df.head()


# ## Player Count

# * Display the total number of players
# 

# In[3]:


totalplayers = purchasedata_df["SN"].nunique()
pd.DataFrame({"Total Players":[totalplayers]})


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


totalitems = purchasedata_df["Item ID"].nunique()
avgprice = purchasedata_df["Price"].mean()
purchasecount = purchasedata_df["Purchase ID"].count()
totalrevenue = purchasedata_df["Price"].sum()
summary_df = pd.DataFrame({"Number of Unique Items":[totalitems], 
                           "Average Price":[avgprice],
                           "Number of Purchases":[purchasecount],
                           "Total Revenue":[totalrevenue]})
summary_df.style.format({"Average Price":"${:,.2f}", "Total Revenue":"${:,.2f}"})


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[5]:


eachuser = purchasedata_df.drop_duplicates(subset=["SN"],keep='first',inplace=False)
gendergroup = eachuser.groupby(["Gender"])
genderdemo_df = pd.DataFrame(gendergroup.count())
genderdemo_df["Total Count"] = genderdemo_df["SN"]
genderdemo_df["Percentage of Players"] = ((genderdemo_df["Total Count"] / genderdemo_df["Total Count"].sum())*100)
newgender_df = genderdemo_df[["Total Count", "Percentage of Players"]]
newgender_df.style.format({"Percentage of Players":"{:.2f}%"})


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[6]:


newgroup = purchasedata_df.groupby(["Gender"])
totalpurchase = newgroup["Price"].sum()
avgprice = totalpurchase / newgroup["Gender"].count()
avgpurchasetotal = totalpurchase / newgroup["SN"].nunique()
gpurchasecount = newgroup["Purchase ID"].count()
newgroupdf = pd.DataFrame({"Purchase Count": gpurchasecount,
                          "Average Purchase Price": avgprice,
                          "Total Purchase Value": totalpurchase,
                          "Avg Total Purchase per Person": avgpurchasetotal})
newgroupdf.style.format({"Average Purchase Price":"${:.2f}","Total Purchase Value":"${:.2f}","Avg Total Purchase per Person":"{:.2f}%"})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[7]:


agebins = [0, 9 , 14, 19, 24, 29, 34, 39, 45]
agelabels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchasedata_df["Age Range"] = pd.cut(purchasedata_df["Age"], agebins, labels=agelabels)
agerange = purchasedata_df.groupby("Age Range")["SN"].nunique()

age = pd.DataFrame(agerange)
playerpercent = ((age["SN"]/totalplayers)*100)
age["Percent of Players"]= playerpercent

age = age.rename(columns={"SN" : "Total Count"})
age.style.format({"Percent of Players":"{:.2f}%"})


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[50]:


agegroup = purchasedata_df.groupby(["Age Range"])
agavgeprice = agegroup["Price"].mean()
agtotalp = agegroup["Price"].sum()
agpurchasecount = agegroup["Price"].count()
perperson = agtotalp/agegroup["SN"].nunique()

summary = pd.DataFrame({"Purchase Count":agpurchasecount,
                     "Average Purchase Price":agavgeprice,
                     "Total Purchase Value":agtotalp,
                     "Avg Total Purchase per Person":perperson})
summary.style.format({"Average Purchase Price":"${:.2f}","Total Purchase Value":"${:.2f}","Avg Total Purchase per Person":"${:.2f}"})


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[41]:


topspend = purchasedata_df.groupby(["SN"])
tspcount = topspend["Purchase ID"].count()
tsavgprice = topspend["Price"].mean()
tstotalvalue = topspend["Price"].sum()
topspenders = pd.DataFrame({"Purchase Count":tspcount,
                           "Average Purchase Price":tsavgprice,
                           "Total Purchase Value":tstotalvalue})

sortspenders = topspenders.sort_values("Total Purchase Value", ascending=False).head()
sortspenders.style.format({"Average Purchase Price":"${:.2f}","Total Purchase Value":"${:.2f}"})


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[38]:



items = purchasedata_df[["Purchase ID","Item ID","Item Name", "Price"]]
grouped_items = items.groupby(["Item ID", "Item Name"])
itempcount = grouped_items["Purchase ID"].count()
itemprice = grouped_items["Price"].sum() / grouped_items["Price"].count()
totalpvalue = grouped_items["Price"].sum()
itemgroup = pd.DataFrame({"Purchase Count":itempcount,
                             "Item Price":itemprice,
                             "Total Purchase Value":totalpvalue})
sortitems = itemgroup.sort_values("Purchase Count", ascending=False).head()
sortitems.style.format({"Item Price":"${:.2f}","Total Purchase Value":"${:.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[40]:


profitable = itemgroup.sort_values("Total Purchase Value", ascending=False).head()
profitable.style.format({"Item Price":"${:.2f}","Total Purchase Value":"${:.2f}"})


# In[ ]:




