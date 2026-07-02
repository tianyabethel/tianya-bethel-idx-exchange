#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
from pathlib import Path

os.chdir("/Users/tianyabethel/Desktop/csv")

data_folder = Path(".")

print("Current folder:", os.getcwd())


# In[8]:


import pandas as pd

sold_data = []
listing_data = []


# In[9]:


for year in [2024, 2025, 2026]:
    end_month = 5 if year == 2026 else 12

    for month in range(1, end_month + 1):
        yyyymm = f"{year}{month:02d}"

        sold_file = data_folder / f"CRMLSSold{yyyymm}.csv"
        listing_file = data_folder / f"CRMLSListing{yyyymm}.csv"

        if sold_file.exists():
            sold_data.append(pd.read_csv(sold_file, low_memory=False))
        else:
            print("Missing sold file:", sold_file.name)

        if listing_file.exists():
            listing_data.append(pd.read_csv(listing_file, low_memory=False))
        else:
            print("Missing listing file:", listing_file.name)


# In[10]:


sold = pd.concat(sold_data, ignore_index=True)
listing = pd.concat(listing_data, ignore_index=True)

print("Sold rows before filter:", len(sold))
print("Listing rows before filter:", len(listing))


# In[12]:


sold = sold[sold["PropertyType"] == "Residential"]
listing = listing[listing["PropertyType"] == "Residential"]

print("Sold rows after filter:", len(sold))
print("Listing rows after filter:", len(listing))


# In[13]:


sold.to_csv("combined_sold_residential.csv", index=False)
listing.to_csv("combined_listing_residential.csv", index=False)

print("Done! Files saved.")


# In[ ]:




