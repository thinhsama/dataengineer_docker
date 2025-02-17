from bs4 import BeautifulSoup
import requests
import pandas as pd
html_page = requests.get('https://books.toscrape.com/')
soup = BeautifulSoup(html_page.content, 'html.parser')
#soup.prettify()
warning = soup.find('div', class_='alert alert-warning')
print(warning.text)
book_container = warning.nextSibling.nextSibling 
titles = book_container.findAll('h3') # Make a selection
titles[0] # Preview the first entry it
print(titles[0].text)
titles[0].find('a')
print(titles[0].find('a'))
print(titles[0].find('a').attrs['title'])
final_titles = [h3.find('a').attrs['title'] for h3 in book_container.findAll('h3')]
print(len(final_titles), final_titles[:5])
import re
regex = re.compile("star-rating (.*)")
book_container.findAll('p', {"class" : regex}) # Initial Trial in developing the script
star_ratings = []
for p in book_container.findAll('p', {"class" : regex}):
    star_ratings.append(p.attrs['class'][-1])
print(star_ratings)
star_dict = {'One': 1, 'Two': 2, 'Three':3, 'Four': 4, 'Five':5} # Manually create a dictionary to translate to numeric
star_ratings = [star_dict[s] for s in star_ratings]
print(star_ratings)
book_container.findAll('p', class_="price_color") # First preview
prices = [p.text for p in book_container.findAll('p', class_="price_color")] # Keep cleaning it up
print(len(prices), prices[:5])
prices = [float(p[1:]) for p in prices] # Removing the pound sign and converting to float
print(len(prices), prices[:5])
avails = book_container.findAll('p', class_="instock availability")
avails[:5] # Preview our selection
avails = [a.text.strip() for a in book_container.findAll('p', class_="instock availability")] # Finalize the selection
print(len(avails), avails[:5])
# Putting it All Together
df = pd.DataFrame([final_titles, star_ratings, prices, avails]).transpose()
df.columns = ['Title', 'Star_Rating', 'Price_(pounds)', 'Availability']
print(df.head())