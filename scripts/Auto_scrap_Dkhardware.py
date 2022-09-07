# Python project for pricing scripping of different sites
# Creado por: Camilo Pardo Macea

# FOR DKhardware
# ----------------------------------------------------------------------------------------------------------------------
# Libraries import
# ----------------------------------------------------------------------------------------------------------------------
import datetime
import os
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# Configuration and Global Variables
# ----------------------------------------------------------------------------------------------------------------------
# Path definition of the .csv file
fecha = datetime.datetime.today()
folder = fecha.strftime('%Y-%m')
if not os.path.exists('./XX_Data/' + folder):
    os.makedirs('./XX_Data/' + folder)
output_path_toilet = './XX_Data/' + folder + '/Dkhardware_toilet-' + str(fecha.year) + '_' + str(fecha.month) + '.csv'

# Path for loading the URL sites
url_path_toilet = './XX_Url/Dkhardware.xlsx'

# Number of retry
NUM_RETRIES = 5

# Waiting time between request
delays = [1, 4, 8, 2, 5, 3]

# Header for beautiful soup
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}


# Function for data extract informacion of product
def Dkhardware_data(elem, soup_html):
    """
    Programa que toma la información general de una página de producto del market place de DKhardware
    """
    # Collecting the name and product type
    brand_name = elem["Fabricante"]
    product_name = elem["Short Name"]
    product_format = elem["Type"]
    # brand_name = soup_html.find('div', class_='product-detail__brand-container').text.strip()
    # product_name = soup_html.find('meta', {'property':'og:title'}).attrs['content']

    # Collecting the sku
    # sku_ref = soup_html.find('div', class_='product-number').find('span', class_='itemNumber').text
    internet_ref = soup_html.find('p', class_='item-code')
    internet_ref = internet_ref.find('span').text.split(' ')[0]

    # Collecting the current price
    price_clean = soup_html.find('p', class_='price').text.split(' ')[15].split('$')[1].strip()

    # Collecting the image
    url_img = soup_html.find('meta', {'property': 'og:image'}).attrs['content']

    # Stock Online
    try:
        stock_flag = soup_html.find('span', class_='stock-text').text
        #print(stock_flag)
        if stock_flag is None:
            stock = 'No'
        else:
            stock = 'Si'
    except:
        stock = "Na"
    # ------------------------------------------------------------------------------------------------------------------
    # Message display
    print("Recopilando la información de {}".format(elem["Link"]))
    # print("La marca es la: {}".format(brand_name))
    print("El sanitario es el: {}".format(product_name))
    print("El tipo de producto es un: {}".format(product_format))
    # print("El sku es el: {}".format(sku_ref))
    print("El sku_internet es el: {}".format(internet_ref))
    print("El precio listado es: {} USD".format(price_clean))
    print("El stock es: {}".format(stock))
    print(url_img)
    print("\n")
    # ------------------------------------------------------------------------------------------------------------------
    # Appending the item in a list
    information = [datetime.datetime.today().date(), brand_name, elem["Sku"],
                   elem["Linea"], product_format, elem["Rough in"], elem["Bowl Height"], elem["Asiento"],
                   elem["Capacidad (Gpl)"], product_name, internet_ref,
                   price_clean, "USD", "dkhardware.com", stock, elem["Link"], url_img]

    return information

# ----------------------------------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------------------------------
for product_type, output_path in [[url_path_toilet, output_path_toilet]]:
    # Reading .xlsx file with url list
    file_df = pd.read_excel(product_type)

    # Keeping just the row with links
    product_df = file_df[file_df['Link'].notna()]

    # Scrapping the information of every url
    data = []
    for index, elem in product_df.iterrows():
        for i in range(NUM_RETRIES):
            # Random Wait between request
            delay = np.random.choice(delays)
            time.sleep(delay)
            try:
                response = requests.get(elem["Link"], headers=headers)

                print("Intento numero {}".format(i))
                print(response)
                if response.status_code in [200, 404]:
                    # escape for loop if the API returns a successful response
                    break
            except requests.exceptions.ConnectionError:
                response = ''
                print("ConnectionError")
        try:
            estate = response.status_code
        except:
            estate = 900

        # parse data if 200 status code (successful response)
        if estate == 200:
            # Parse data with beautifulsoup
            soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

            # Getting the information from the website
            toilet_information = Dkhardware_data(elem, soup)
            data.append(toilet_information)

    # Creating the dataframe
    df = pd.DataFrame(data, columns=["Fecha", "Fabricante", "SKU", "Linea", "Tipo", "Rough_In",
                                     "Bowl Height", "Asiento", "Capacidad (Gpl)", "Producto",
                                     "Cod_Internet", "Precio", "Moneda",
                                     "Market_Place", "Stock", "URL", "Image_url"])

    # Saving the file in a .csv file
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)
