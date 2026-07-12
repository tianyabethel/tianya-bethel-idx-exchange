#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os

os.chdir("/Users/tianyabethel/Desktop/csv")

print(os.getcwd())


# In[3]:


from pathlib import Path

print(Path("combined_sold_residential.csv").exists())
print(Path("combined_listing_residential.csv").exists())


# In[5]:


import pandas as pd

sold = pd.read_csv(
    "combined_sold_residential.csv",
    low_memory=False
)

listing = pd.read_csv(
    "combined_listing_residential.csv",
    low_memory=False
)


# In[8]:


url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(url)

mortgage.columns = ["date", "rate_30yr_fixed"]

mortgage["date"] = pd.to_datetime(mortgage["date"])


# In[9]:


mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()


# In[10]:


sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")

listing["year_month"] = pd.to_datetime(listing["ListingContractDate"]).dt.to_period("M")


# In[11]:


sold = sold.merge(mortgage_monthly, on="year_month", how="left")

listing = listing.merge(mortgage_monthly, on="year_month", how="left")


# In[12]:


print(sold["rate_30yr_fixed"].isna().sum())
print(listing["rate_30yr_fixed"].isna().sum())


# In[13]:


sold.to_csv("combined_sold_residential_with_rates.csv", index=False)

listing.to_csv("combined_listing_residential_with_rates.csv", index=False)

print("Done!")


# In[ ]:




