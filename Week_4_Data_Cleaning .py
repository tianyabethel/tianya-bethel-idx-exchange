#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os

os.chdir("/Users/tianyabethel/Desktop/csv")
print(os.getcwd())


# In[7]:


sold = pd.read_csv("combined_sold_residential_with_rates.csv")
listing = pd.read_csv("combined_listing_residential_with_rates.csv")


# In[8]:


print("Sold shape:", sold.shape)
print("Listing shape:", listing.shape)


# In[10]:


date_columns = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for col in date_columns:
    if col in sold.columns:
        sold[col] = pd.to_datetime(sold[col], errors="coerce")

    if col in listing.columns:
        listing[col] = pd.to_datetime(listing[col], errors="coerce")


# In[19]:


print(sold[date_columns].dtypes)
print(listing[date_columns].dtypes)


# In[11]:


duplicate_pairs = [
    ("PropertyType", "PropertyType.1"),
    ("ListPrice", "ListPrice.1"),
    ("LivingArea", "LivingArea.1"),
    ("CloseDate", "CloseDate.1"),
    ("BuyerOfficeName", "BuyerOfficeName.1"),
    ("ListAgentFirstName", "ListAgentFirstName.1"),
    ("ListAgentLastName", "ListAgentLastName.1"),
    ("Longitude", "Longitude.1"),
    ("Latitude", "Latitude.1"),
    ("DaysOnMarket", "DaysOnMarket.1")
]

for original, duplicate in duplicate_pairs:
    if duplicate in listing.columns:
        print(original, listing[original].equals(listing[duplicate]))


# In[16]:


print("CloseDate identical:",
      listing["CloseDate"].equals(listing["CloseDate.1"]))

print("BuyerOfficeName identical:",

      listing["BuyerOfficeName"].equals(listing["BuyerOfficeName.1"]))


# In[17]:


listing.drop(columns=[
    "PropertyType.1",
    "ListPrice.1",
    "LivingArea.1",
    "ListAgentFirstName.1",
    "ListAgentLastName.1",
    "Longitude.1",
    "Latitude.1",
    "DaysOnMarket.1"
], inplace=True)

print("Duplicate columns removed.")


# In[18]:


sold_rows_before = len(sold)
listing_rows_before = len(listing)

print("Sold rows before cleaning:", sold_rows_before)
print("Listing rows before cleaning:", listing_rows_before)


# In[20]:


sold_all_missing = sold.columns[sold.isna().all()].tolist()
listing_all_missing = listing.columns[listing.isna().all()].tolist()

print("Sold columns removed:", sold_all_missing)
print("Listing columns removed:", listing_all_missing)

sold = sold.drop(columns=sold_all_missing)
listing = listing.drop(columns=listing_all_missing)


# In[27]:


numeric_columns = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "DaysOnMarket",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "Latitude",
    "Longitude",
    "YearBuilt"
]

for col in numeric_columns:
    if col in sold.columns:
        sold[col] = pd.to_numeric(sold[col], errors="coerce")

    if col in listing.columns:
        listing[col] = pd.to_numeric(listing[col], errors="coerce")


# In[24]:


for df in [sold, listing]:
    df["invalid_close_price_flag"] = df["ClosePrice"].notna() & (df["ClosePrice"] <= 0)
    df["invalid_living_area_flag"] = df["LivingArea"].notna() & (df["LivingArea"] <= 0)
    df["negative_days_on_market_flag"] = df["DaysOnMarket"].notna() & (df["DaysOnMarket"] < 0)
    df["negative_bedrooms_flag"] = df["BedroomsTotal"].notna() & (df["BedroomsTotal"] < 0)
    df["negative_bathrooms_flag"] = (
        df["BathroomsTotalInteger"].notna()
        & (df["BathroomsTotalInteger"] < 0)
    )


# In[25]:


for df in [sold, listing]:
    df["listing_after_close_flag"] = (
        df["ListingContractDate"].notna()
        & df["CloseDate"].notna()
        & (df["ListingContractDate"] > df["CloseDate"])
    )

    df["purchase_after_close_flag"] = (
        df["PurchaseContractDate"].notna()
        & df["CloseDate"].notna()
        & (df["PurchaseContractDate"] > df["CloseDate"])
    )

    df["negative_timeline_flag"] = (
        df["ListingContractDate"].notna()
        & df["PurchaseContractDate"].notna()
        & (df["ListingContractDate"] > df["PurchaseContractDate"])
    )


# In[26]:


for df in [sold, listing]:
    df["missing_coordinates_flag"] = (
        df["Latitude"].isna() | df["Longitude"].isna()
    )

    df["zero_coordinates_flag"] = (
        (df["Latitude"] == 0) | (df["Longitude"] == 0)
    )

    df["positive_longitude_flag"] = df["Longitude"] > 0

    df["implausible_coordinates_flag"] = (
        df["Latitude"].notna()
        & df["Longitude"].notna()
        & (
            ~df["Latitude"].between(32, 42.5)
            | ~df["Longitude"].between(-125, -114)
        )
    )


# In[28]:


flag_columns = [
    "invalid_close_price_flag",
    "invalid_living_area_flag",
    "negative_days_on_market_flag",
    "negative_bedrooms_flag",
    "negative_bathrooms_flag",
    "listing_after_close_flag",
    "purchase_after_close_flag",
    "negative_timeline_flag",
    "missing_coordinates_flag",
    "zero_coordinates_flag",
    "positive_longitude_flag",
    "implausible_coordinates_flag"
]

print("SOLD FLAG COUNTS")
print(sold[flag_columns].sum())

print("\nLISTING FLAG COUNTS")
print(listing[flag_columns].sum())

print("\nSold rows before/after:", sold_rows_before, len(sold))
print("Listing rows before/after:", listing_rows_before, len(listing))


# In[29]:


sold.to_csv("cleaned_sold_residential.csv", index=False)
listing.to_csv("cleaned_listing_residential.csv", index=False)

print("Cleaned datasets saved.")


# In[ ]:




