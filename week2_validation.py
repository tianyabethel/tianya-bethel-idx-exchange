#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import pandas as pd

os.chdir("/Users/tianyabethel/Desktop/csv")
print(os.getcwd())


# In[11]:


sold = pd.read_csv("combined_sold_residential.csv", low_memory=False)
listing = pd.read_csv("combined_listing_residential.csv", low_memory=False)

print("Sold shape:", sold.shape)
print("Listing shape:", listing.shape)


# In[12]:


print("Sold columns:")
print(sold.columns)

print("\nListing columns:")
print(listing.columns)

print("\nSold data types:")
print(sold.dtypes)

print("\nListing data types:")
print(listing.dtypes)


# In[13]:


print("Sold property types:")
print(sold["PropertyType"].unique())

print("\nListing property types:")
print(listing["PropertyType"].unique())


# In[14]:


sold_missing = pd.DataFrame({
    "missing_count": sold.isnull().sum(),
    "missing_percent": sold.isnull().mean() * 100
}).sort_values("missing_percent", ascending=False)

listing_missing = pd.DataFrame({
    "missing_count": listing.isnull().sum(),
    "missing_percent": listing.isnull().mean() * 100
}).sort_values("missing_percent", ascending=False)

print("Sold missing value report:")
print(sold_missing)

print("\nListing missing value report:")
print(listing_missing)


# In[15]:


sold_over_90 = sold_missing[sold_missing["missing_percent"] > 90]
listing_over_90 = listing_missing[listing_missing["missing_percent"] > 90]

print("Sold columns over 90% missing:")
print(sold_over_90)

print("\nListing columns over 90% missing:")
print(listing_over_90)


# In[16]:


numeric_fields = ["ClosePrice", "LivingArea", "DaysOnMarket"]

sold_numeric_summary = sold[numeric_fields].describe(
    percentiles=[0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
)

print("Sold numeric summary:")
print(sold_numeric_summary)


# In[17]:


sold_missing.to_csv("sold_missing_value_report.csv")
listing_missing.to_csv("listing_missing_value_report.csv")

sold_numeric_summary.to_csv("sold_numeric_distribution_summary.csv")

sold.to_csv("sold_week2_filtered.csv", index=False)
listing.to_csv("listing_week2_filtered.csv", index=False)

print("Week 2 files saved.")


# In[ ]:




