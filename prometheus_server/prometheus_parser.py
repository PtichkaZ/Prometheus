#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

service_name = 'prometheus'
os = 'linux'
arch = 'amd64'

html_text = requests.get('https://prometheus.io/download/').text

soup = BeautifulSoup(html_text, 'lxml')

services = []
for service in soup.find_all('h2', id=True):
    services.append(service['id'])
    
all_data = []
for sibling in soup.find_all(class_='table table-bordered downloads'):
    for i in sibling.find_all('tbody'):
        service_data = []
        data = i.find_all('tr')
        for d in data:
            part = []
            part.append(dict(zip(['data-arch', 'data-os', 'link', 'checksum'], 
                                     [d['data-arch'], d['data-os'], d.find('a', class_="download", href=True)['href'], 
                                      d.find('td', class_="checksum").text])))
            service_data.append(part)  
        all_data.append(service_data)

for ser, data in zip(services, all_data):
    if ser == service_name:
        for i in range (0, len(data)):
            if data[i][0]['data-os'] == os and data[i][0]['data-arch'] == arch:
                print(data[i][0]['link'])
                print(data[i][0]['checksum'])            
