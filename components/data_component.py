# Project Pricing Mansfield
# data load and transformation
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import os

import pandas as pd


# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def load_data(filename):
    """
    Función que carga el archivo csv guardado al conectar con la base de datos y devuelve un dataframe
    """
    df = pd.read_csv(filename)

    return df


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
    df = pd.concat([df, load_data(filename=file)])

# Dropping duplicates in case the robot take two values by day
df.drop_duplicates(inplace=True)

# Creating a new product name combining the product name + sku
df['Producto_sku'] = ['_'.join(i) for i in zip(df['Producto'], df['SKU'].map(str))]

# String the SKU
df['SKU_str'] = df['SKU'].map(str)

# ----------------------------------------------------------------------------------------------------------------------
# Master database
# ----------------------------------------------------------------------------------------------------------------------
# Loading the Master Database
# Reading files with the directory for comparisons
comp_df = pd.read_excel('./data/Productos Mansfield.xlsx')

# Organizing the SKU
comp_df['Homologo'] = comp_df['Homologo Mansfield'].map(str)
comp_df['Homologo'] = comp_df['Homologo'].apply(lambda x: x.strip())

# Mansfield df Summary products
sku_list_mansfield = ['130010007', '135010007', '137210040', '160010007', '384010000', '386010000']

Mansfield_df = df[df["Fabricante"] == 'Mansfield']
Mansfield_df = Mansfield_df[Mansfield_df['SKU_str'].isin(sku_list_mansfield)]