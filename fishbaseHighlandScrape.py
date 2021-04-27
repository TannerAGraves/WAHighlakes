# %% INIT
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url_base = "https://wdfw.wa.gov/fishing/locations/high-lakes?name=&county=All&species=&page={page_num}"
lake_name = []
lake_url = []
lake_acrage = []
lake_elevation = []
lake_county = []
lake_loc = []
page_sp = requests.get(url_base.format(page_num=0)).content
soup = BeautifulSoup(page_sp, 'html.parser')
pages_elm = soup.find(class_="pager__item pager__item--last") # title = "Go to last page"
num_pages = [int(i) for i in pages_elm.text.split() if i.isdigit()][0] # extract int from text
num_lakes = int(soup.find(class_="view-footer").text.split()[-1]) # Get total num of lakes
    
# %% SCRAPE
for pg in range(num_pages):
    print(pg)
    page_sp = requests.get(url_base.format(page_num=pg)).content
    soup = BeautifulSoup(page_sp, 'html.parser')
    lakes_table = soup.find(class_="tablesaw")
    lakes_table = lakes_table.find_all('tr') # parse table into rows
    lakes_table = [lake_row.find_all('td') for lake_row in lakes_table] # parse rows into cols. First row is headers
    lakes_table.pop(0)
    for row in lakes_table:
        lake_name.append(row[0].text.strip())
        lake_url.append("https://wdfw.wa.gov" + row[0].find('a', href=True)['href'])
        acrage = row[1].text.split()
        acrage = acrage[0] if acrage else None
        lake_acrage.append(acrage)
        elevation = row[2].text.split()
        elevation = int(elevation[0]) if elevation else None
        lake_elevation.append(elevation)
        lake_county.append(row[3].text.strip())
        lake_loc.append(row[4].text.strip())
    time.sleep(0.3)

# %% PANDAS
lakes_df = pd.DataFrame({
    'name':lake_name,
    'acrage':lake_acrage,
    'elevation':lake_elevation,
    'loc':lake_loc,
    'url':lake_url
})
# %%
