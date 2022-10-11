# Project Pricing Mansfield
# Data load and transformation
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import os
import numpy as np
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------
# Folder path definition
directory = './data_price'
# ----------------------------------------------------------------------------------------------------------------------
# Price database
# ----------------------------------------------------------------------------------------------------------------------
# Loading the files
files_list = []
for path, _, files in os.walk(directory):
    for name in files:
        files_list.append(os.path.join(path, name))

# Empty data frame
df = pd.DataFrame()

# Loading the DF of each month in a unique DF
for file in files_list:
    df = pd.concat([df, pd.read_csv(file)])

# Dropping duplicates in case the robot take two values by day
df.drop_duplicates(inplace=True)

# Cleaning the product name for empty trilling space
df['Producto'] = df['Producto'].apply(lambda x: x.strip())

# Creating a new product name combining the product name + sku
df['Producto_sku'] = ['_'.join(i) for i in zip(df['Producto'], df['SKU'].map(str))]

# String the SKU
df['SKU_str'] = df['SKU'].map(str)

# Calculating the wholesaler price
df['Precio_wholesaler'] = np.round(df['Precio_Lista'] * df['Multiplicador'], 2)

# ----------------------------------------------------------------------------------------------------------------------
# Master database Competitors
# ----------------------------------------------------------------------------------------------------------------------
# Reading files for competitors
comp_df = pd.read_excel('./data/Wholesaler_Database.xlsx', sheet_name='Competitors')

# Organizing the SKU homologo
comp_df['Homologo'] = comp_df['Homologo Mansfield'].map(str)
comp_df['Homologo'] = comp_df['Homologo'].apply(lambda x: x.strip())

# String the SKU
comp_df['Sku'] = comp_df['Sku'].map(str)
comp_df['Sku'] = comp_df['Sku'].apply(lambda x: x.strip())

# ----------------------------------------------------------------------------------------------------------------------
# Master database Mansfield
# ----------------------------------------------------------------------------------------------------------------------
# Reading files for mansfield
mansfield_df = pd.read_excel('./data/Wholesaler_Database.xlsx', sheet_name='Mansfield')

# Organizing the SKU
mansfield_df['Sku'] = mansfield_df['Sku'].map(str)
mansfield_df['Sku'] = mansfield_df['Sku'].apply(lambda x: x.strip())
