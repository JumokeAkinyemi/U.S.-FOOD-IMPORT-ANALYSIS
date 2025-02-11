#!/usr/bin/env python
# coding: utf-8

# # U.S. FOOD IMPORT ANALYSIS

# The global food trade is a crucial component of the U.S. economy, impacting supply chains, pricing, and consumer choices. This analysis explores food import trends using publicly available data from Data.gov. The dataset provides insights into the total value of U.S. food imports across different years, commodities, and countries. By analyzing trends, we can identify which food items are most imported, which countries contribute the most, and how import patterns change over time.

# # Importing Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_csv(r'C:\Users\user\OneDrive\Desktop\FoodImports.csv')


# In[3]:


# Data Cleaning
df.columns = df.columns.str.strip()
df_cleaned = df.dropna(subset=["Value"])  # Removing missing values in 'Value'


# In[4]:


# Convert 'Year Number' to integer where applicable
df_cleaned = df_cleaned[df_cleaned["Year Number"].astype(str).str.isnumeric()]
df_cleaned["Year Number"] = df_cleaned["Year Number"].astype(int)


# In[19]:


# Summing the total import values per year
yearly_imports = df.groupby('Year Number')['Value'].sum()

# Calculating summary statistics
mean_import_value = yearly_imports.mean()
max_import_value = yearly_imports.max()
min_import_value = yearly_imports.min()

print(f"Mean annual import value: ${mean_import_value:.2f} million")
print(f"Maximum import value: ${max_import_value:.2f} million")
print(f"Minimum import value: ${min_import_value:.2f} million")


# In[6]:


# Total Import Trends Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_cleaned.groupby("Year Number")["Value"].sum(), marker="o", color="b")
plt.title("Total U.S. Food Imports Over the Years", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Total Import Value (Million $)", fontsize=12)
plt.xticks(rotation=45)
plt.show()


# In[7]:


# Top Imported Commodities
top_commodities = df_cleaned.groupby("Commodity")["Value"].sum().nlargest(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_commodities.values, y=top_commodities.index, palette="viridis")
plt.title("Top 10 Imported Commodities by Value", fontsize=14)
plt.xlabel("Total Import Value (Million $)", fontsize=12)
plt.ylabel("Commodity", fontsize=12)
plt.show()


# In[8]:


# Top Exporting Countries (Excluding Aggregated "WORLD" Values)
top_countries = df_cleaned[~df_cleaned["Country"].isin(["WORLD", "WORLD (Quantity)", "REST OF WORLD"])].groupby("Country")["Value"].sum().nlargest(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="coolwarm")
plt.title("Top 10 Countries Contributing to U.S. Food Imports", fontsize=14)
plt.xlabel("Total Import Value (Million $)", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.show()


# In[10]:


# Most Profitable Food Categories (Highest Total Import Value)
top_profitable_categories = df_cleaned.groupby("Category")["Value"].sum().nlargest(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_profitable_categories.values, y=top_profitable_categories.index, palette="coolwarm")
plt.title("Top 10 Most Profitable Food Categories by Import Value", fontsize=14)
plt.xlabel("Total Import Value (Million $)", fontsize=12)
plt.ylabel("Category", fontsize=12)
plt.show()


# In[11]:


# Correlation Analysis
# Selecting numerical columns for correlation
correlation_matrix = df_cleaned[["Year Number", "Value"]].corr()
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Analysis of Variables", fontsize=14)
plt.show()


# In[12]:


# Yearly Import Trends for Top 5 Countries
top_5_countries = (
    df_cleaned[~df_cleaned["Country"].isin(["WORLD", "WORLD (Quantity)", "REST OF WORLD"])]
    .groupby("Country")["Value"]
    .sum()
    .nlargest(5)
    .index
)

df_top_countries = df_cleaned[df_cleaned["Country"].isin(top_5_countries)]
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_top_countries.groupby(["Year Number", "Country"])["Value"].sum().reset_index(),
    x="Year Number",
    y="Value",
    hue="Country",
    marker="o",
    palette="tab10"
)
plt.title("Yearly Import Trends for Top 5 Countries", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Total Import Value (Million $)", fontsize=12)
plt.legend(title="Country")
plt.xticks(rotation=45)
plt.show()


# In[13]:


# Yearly Trends for Top 5 Commodities
top_5_commodities = df_cleaned.groupby("Commodity")["Value"].sum().nlargest(5).index
df_top_commodities = df_cleaned[df_cleaned["Commodity"].isin(top_5_commodities)]

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_top_commodities.groupby(["Year Number", "Commodity"])["Value"].sum().reset_index(),
    x="Year Number",
    y="Value",
    hue="Commodity",
    marker="o",
    palette="Set1"
)
plt.title("Yearly Trends for Top 5 Commodities", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Total Import Value (Million $)", fontsize=12)
plt.legend(title="Commodity")
plt.xticks(rotation=45)
plt.show()


# In[14]:


# Price per Unit Analysis
if "WORLD (Quantity)" in df_cleaned["Country"].unique():
    df_quantity = df_cleaned[df_cleaned["Country"] == "WORLD (Quantity)"].copy()
    df_quantity.rename(columns={"Value": "Total Quantity"}, inplace=True)

    df_value = df_cleaned[df_cleaned["Country"] == "WORLD"].copy()
    df_value.rename(columns={"Value": "Total Import Value"}, inplace=True)

    df_price_per_unit = pd.merge(df_value[["Year Number", "Total Import Value"]], df_quantity[["Year Number", "Total Quantity"]], on="Year Number", how="inner")
    df_price_per_unit["Price per Unit"] = df_price_per_unit["Total Import Value"] / df_price_per_unit["Total Quantity"]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_price_per_unit, x="Year Number", y="Price per Unit", marker="o", color="r")
    plt.title("Trend of Price per Unit for Imported Food Products", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Price per Unit ($ per unit)", fontsize=12)
    plt.xticks(rotation=45)
    plt.show()


# In[15]:


# Trends for WORLD, WORLD (Quantity), and REST OF WORLD
df_world = df_cleaned[df_cleaned["Country"] == "WORLD"]
df_world_quantity = df_cleaned[df_cleaned["Country"] == "WORLD (Quantity)"]
df_rest_of_world = df_cleaned[df_cleaned["Country"] == "REST OF WORLD"]

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_world.groupby("Year Number")["Value"].sum(), label="WORLD", marker="o", color="b")
sns.lineplot(data=df_world_quantity.groupby("Year Number")["Value"].sum(), label="WORLD (Quantity)", marker="s", color="g")
sns.lineplot(data=df_rest_of_world.groupby("Year Number")["Value"].sum(), label="REST OF WORLD", marker="^", color="r")
plt.title("Import Trends: WORLD vs WORLD (Quantity) vs REST OF WORLD", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Total Import Value (Million $)", fontsize=12)
plt.legend(title="Category")
plt.xticks(rotation=45)
plt.show()


# In[ ]:




