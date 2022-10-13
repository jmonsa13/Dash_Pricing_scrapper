# Project Pricing Mansfield
# Price Index component
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def price_index_calculation(df_comp, df_mansfield):
    """
    Función que calcula el price index history based on a mansfield product
        :param df_comp: pandas dataframe  containing the information from the competitors
        :param df_mansfield: pandas dataframe  containing the information from mansfields
        :return: A list with the price index information for the competitors
    """
    # ----------------------------------------------------------------------------------------------------------
    # Price Index
    # ----------------------------------------------------------------------------------------------------------
    # Calculating the price index for the competitor
    price_index = []
    for index, row in df_comp.iterrows():
        # Recovering the wholesaler price of mansfield for a specific date
        df_mansfield_single = df_mansfield[df_mansfield['Fecha'] == row['Fecha']]
        price_wholesaler_mansfield = df_mansfield_single.iloc[0]['Precio_wholesaler']

        # Math equation for the price index in %
        price_index_value = np.round(((row['Precio_wholesaler'] / price_wholesaler_mansfield) * 100), 2)
        price_index.append(price_index_value)

    return price_index
