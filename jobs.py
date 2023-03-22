import requests
from bs4 import BeautifulSoup
import pprint
import os
import random
import time

url = "https://realpython.github.io/fake-jobs/"

page_content = ''

if not os.path.exists('fake-jobs.html'):
    print("Loading page from the internet...")
    page = requests.get(url)
    page_content = page.content.decode()
    with open('fake-jobs.html', 'w') as outfile:
        outfile.write(page_content)
else:
    print("Reading from file...")
    with open('fake-jobs.html', 'r') as infile:
        page = infile.read()
    page_content = page.encode('utf-8') 

soup = BeautifulSoup(page_content, "html.parser")

jobs = soup.find_all('div', class_ = 'card-content')

jobs_data = []

# def get_text_attribute(bs, tag, class_=None):
#     response_text = bs.find(tag, class_=class_)
#     if response_text:
#         return response_text.text.strip()
#     return ''

for job in jobs:
    job_title = job.find('h2').text.strip()
    company_name = job.find('h3').text.strip()
    location = job.find('p', class_ = 'location')
    if location:
        location = location.text.strip()
        lst = location.split(',')
        city = lst[0]
        province = lst[1].strip()
    date = job.find('time').text.strip()
    # if 'Joshuatown' in location:
    #     print(f'{job_title}, {company_name}, {location}, {date}')
    link_href = ''
    links = job.find_all('a')
    for link in links:
        if link.text == 'Apply':
            link_href = link['href']
    description = ''
    job_detail_content= ''

    filename = link_href.split('/')[-1].strip()

    if not os.path.exists(filename):
        wait_time_in_seconds = random.randint(2,4)
        print(f'Waiting {wait_time_in_seconds} seconds')
        time.sleep(wait_time_in_seconds)
        print(f'Loading {filename} page...')

        job_detail_page = requests.get(link_href)
        job_detail_content = job_detail_page.content.decode()

        with open(filename, 'w') as outfile:
            outfile.write(job_detail_content)
    else:
        with open(filename, 'r') as infile:
            job_detail_page = infile.read()
        job_detail_content = job_detail_page.encode("utf-8") 

    job_soup = BeautifulSoup(job_detail_content, 'html.parser')
    content_soup = job_soup.find('div', class_='content') 
    description = content_soup.find('p').text.strip()

    next_job = {
        'job_title':job_title,
        'company_name': company_name,
        'description':description,
        'city':city,
        'province':province,
        'date_posted':date,
        'apply_link':link_href
    }
    jobs_data.append(next_job)
    # print(next_job)

    # print(f'{job_title}, {company_name}, {location}, {date}\n{link_href}\n\n')
pprint.pprint(jobs_data)