import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrape():
    url = 'https://www.example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
if __name__ == '__main__':
    soup = scrape()
    #print(soup.prettify())
    title = soup.find('title')
    print(title.text)
    title1 = soup.select_one('h1').text
    print(title1)
    text = soup.select_one('p').text
    print(text)
    link = soup.select_one('a').get('href')
    print(link)