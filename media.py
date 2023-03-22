import requests
from bs4 import BeautifulSoup
import os
import random
import time
import pprint

url = "https://www.churchofjesuschrist.org/media/collection/bible-videos-nativity?lang=eng"

page_content = ''

if not os.path.exists('media.html'):
    print("Loading page from the internet...")
    page = requests.get(url)
    page_content = page.content.decode()
    with open('media.html', 'w') as outfile:
        outfile.write(page_content)
else:
    print("Reading from file...")
    with open('media.html', 'r') as infile:
        page = infile.read()
    page_content = page.encode('utf-8') 

soup = BeautifulSoup(page_content, 'html.parser')

# assets = soup.find_all('div', class_ = 'sc-8c1lm1-0 jcVfwW')
asset_cards = soup.find_all('a')


asset_data = []

for card in asset_cards:
    title = card.find('div', class_ = 'sc-12mz36o-0 gUtHzi sc-crhpvg-5 aibeu')
    link_href = card['href']
    if title:
        title = title.text.strip()

    asset_detail = ''

    filename = str(title) 

    if not os.path.exists(filename):
        wait_time_in_seconds = random.randint(2,4)
        print(f'Waiting {wait_time_in_seconds} seconds')
        time.sleep(wait_time_in_seconds)
        print(f'Loading {filename} page...')

        asset_detail_page = requests.get(f'https://www.churchofjesuschrist.org/{link_href}')
        asset_detail_content = asset_detail_page.content.decode()

        with open(filename, 'w') as outfile:
            outfile.write(asset_detail_content)
    else:
        with open(filename, 'r') as infile:
            asset_detail_page = infile.read()
        asset_detail_content = asset_detail_page.encode("utf-8")

    asset_soup = BeautifulSoup(asset_detail_content, 'html.parser')
    content_soup = asset_soup.find('div', class_='sc-9dd4b4e5-1 jBFjPW') 

    description = ''
    if content_soup:
        description = content_soup.find('div', class_ = 'sc-1szn76m-0 kFzbNE').text.strip()
        scripture_ref_soup = content_soup.find('div', class_ = 'sc-1u44evz-0 JDVKk')
        print(scripture_ref_soup)
        # refs_array = []
        # if scripture_ref_soup:
        #     scripture_refs = scripture_ref_soup.find('span')
            
            
            # for ref in scripture_refs:
            #     ref = ref.text.strip()
                # refs_array.append(ref)

   
    # tags_soup = asset_soup.find('span', class_ = 'sc-kb0k5s-0 gSUFTs')
    # tags_array = []
    # if tags_soup:
    #     tags = tags_soup.find_all('a')
    #     for tag in tags:
    #         tag = tag.text.strip()
    #         tags_array.append(tag)
    # print(tags_array)

#     next_asset = {
#         'asset_title':title,
#         'description': description,
#         'scripture_ref': ref,
#         'tags': tags_array,
#         'asset_link':f'https://www.churchofjesuschrist.org/{link_href}'
#     }
#     asset_data.append(next_asset)

# pprint.pprint(asset_data)