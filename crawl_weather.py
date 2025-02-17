import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.timeanddate.com/weather/vietnam/hanoi"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("Crawl data successfully")
else:
    print("Error")
    exit()
# parse HTML để lấy dữ liệu thời tiết
soup = BeautifulSoup(response.text, "html.parser")
# in ra dần dần để xem cấu trúc HTML
#print(soup.prettify())
temp = soup.find("div", class_="h2").text.strip()
condition = soup.find("p").text.strip()
extra_info = soup.find_all("tr")
wind_speed = "N/A"
humidity = "N/A"

for row in extra_info:
    columns = row.find_all("td")
    if len(columns) > 1:
        label = row.find("th")  # Lấy tiêu đề của hàng
        value = columns[0].text.strip()  # Lấy giá trị

        if label and "Wind Speed" in label.text:
            wind_speed = value
        if label and "Humidity" in label.text:
            humidity = value

print("Temperature:", temp)
print("Condition:", condition)
print("Wind Speed:", wind_speed)
print("Humidity:", humidity)
