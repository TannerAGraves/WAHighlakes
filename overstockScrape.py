# %% INIT
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url_base = "https://wdfw.wa.gov/fishing/locations/high-lakes/overabundant?name=&county=All&species=&page={page_num}"
over_name = []
over_url = []
page_sp = requests.get(url_base.format(page_num=0)).content
soup = BeautifulSoup(page_sp, 'html.parser')
pages_elm = soup.find(class_="pager__item pager__item--last") # title = "Go to last page"
num_pages = [int(i) for i in pages_elm.text.split() if i.isdigit()][0] # extract int from text

    
# %% SCRAPE
for pg in range(num_pages):
    print(pg)
    page_sp = requests.get(url_base.format(page_num=pg)).content
    soup = BeautifulSoup(page_sp, 'html.parser')
    over_table = soup.find(class_="tablesaw")
    over_table = over_table.find_all('tr') # parse table into rows
    over_table = [lake_row.find_all('td') for lake_row in over_table] # parse rows into cols. First row is headers
    over_table.pop(0)
    for row in over_table:
        over_name.append(row[0].text.strip())
        over_url.append("https://wdfw.wa.gov" + row[0].find('a', href=True)['href'])
    time.sleep(0.3)
# %% PANDAS
over_df = pd.DataFrame({'name':over_name, 'url':over_url})
over_df
# %%
