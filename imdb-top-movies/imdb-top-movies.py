import os

import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm


src_folder_path = os.path.dirname(__file__) # to get current script folder path

year = str(input('Enter year: '))
url = 'http://www.imdb.com/search/title?release_date=' + year + ',' + year + '&title_type=feature'
ourUrl = urllib3.PoolManager().request('GET', url)
print('Status', ourUrl.status)
soup = BeautifulSoup(ourUrl.data, "lxml")

df = {'Movies': [], 'Rating': [], 'Genre': [], 'Link': []}
movieList = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
for div_item in tqdm(movieList):
    div = div_item.find('div', attrs={'class':'lister-item-content'})

    text_muted = div.find('p', class_='text-muted')
    genre = text_muted.find('span', class_='genre').text.strip()

    rating_bar = div.find('div', class_='ratings-bar')
    rating_bar_2 = rating_bar.find('div', class_='inline-block ratings-imdb-rating') if rating_bar is not None else None
    rating_num = float(rating_bar_2.find('strong').text) if rating_bar_2 is not None else None

    header = div.findChildren('h3', attrs={'class':'lister-item-header'})

    df['Movies'].append((header[0].findChildren('a'))[0].contents[0])
    df['Genre'].append(genre)
    df['Rating'].append(rating_num)
    df['Link'].append("https://www.imdb.com" + (header[0].findChildren('a'))[0]['href'])
    # df['Movies'].append(str((header[0].findChildren('a'))[0].contents[0]).encode('utf-8').decode('ascii', 'ignore'))

df = pd.DataFrame(df)
df.index = df.index + 1
df.to_excel(src_folder_path + f'\imdb top movies {year}.xlsx', sheet_name=year, index=True)
