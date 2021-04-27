# %% INIT
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url_base = "https://wdfw.wa.gov/fishing/locations/high-lakes/stocking?county=All&year=All&species=&page={page_num}"
stock_table = []
page_sp = requests.get(url_base.format(page_num=0)).content
soup = BeautifulSoup(page_sp, 'html.parser')
pages_elm = soup.find(class_="pager__item pager__item--last") # title = "Go to last page"
num_pages = [int(i) for i in pages_elm.text.split() if i.isdigit()][0] # extract int from text

    
# %% SCRAPE
for pg in range(num_pages):
    print(pg)
    page_sp = requests.get(url_base.format(page_num=pg)).content
    soup = BeautifulSoup(page_sp, 'html.parser')
    #Granularity lake, species, stock
    dataBody = soup.find(class_="view-content")
    lakes = dataBody.find_all(class_='card') # parse table into lakes
    time.sleep(0.3)
    for lake in lakes:
        stock_lake = lake.find(class_='card-divider').text
        stock_url = "https://wdfw.wa.gov" + lake.find('a', href=True)['href']
        stock_species_lst = lake.find_all(class_='item-list')
        for species in stock_species_lst:
            stock_species = species.text.strip().split('\n')[0]
            plants = species.find_all(class_='field-content')
            for plant in plants:
                (stock_time, stock_amt) = plant.text.strip().split(':')
                #stock_time = plant.find('time')['datetime']
                #stock_amt = plant.text.split()[-1]
                stock_table.append([stock_lake.strip(), stock_species, stock_amt, stock_time.strip(),stock_url])

# %% PANDAS
stock_df = pd.DataFrame(stock_table, columns = ['lake', 'species', 'amount', 'date', 'url'])
stock_df
# %%
