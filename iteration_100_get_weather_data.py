import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL của trang web thời tiết
url = "https://www.timeanddate.com/weather/vietnam/hanoi"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Danh sách lưu dữ liệu
weather_data = []

# Lặp để lấy 100 dòng dữ liệu
for i in range(10):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Tìm nhiệt độ
        temp_element = soup.find("div", class_="h2")
        temperature = temp_element.text.strip() if temp_element else "N/A"

        # Tìm các hàng chứa thông tin thời tiết
        extra_info = soup.find_all("tr")

        wind_speed = "N/A"
        humidity = "N/A"

        for row in extra_info:
            columns = row.find_all("td")
            if len(columns) > 1:
                label = row.find("th")  # Tìm tiêu đề của hàng
                value = columns[0].text.strip()  # Lấy giá trị

                if label and "Wind Speed" in label.text:
                    wind_speed = value
                if label and "Humidity" in label.text:
                    humidity = value
        # in ra
        print('iteration:', i+1)
        print("Temperature:", temperature)
        print("Wind Speed:", wind_speed)
        print("Humidity:", humidity)
        print('wind_speed:', wind_speed)
        # Lưu dữ liệu vào danh sách
        weather_data.append({
            "date": pd.to_datetime("today").strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed
        })

        print(f"Đã lấy dữ liệu lần {i+1}: {temperature}, {humidity}, {wind_speed}")

    else:
        print(f"Lỗi khi lấy dữ liệu ({response.status_code})")
        break  # Nếu lỗi, dừng chương trình

    time.sleep(1)  # Chờ 1 giây để tránh bị chặn

# Chuyển danh sách thành DataFrame
df = pd.DataFrame(weather_data)

# Lưu vào file CSV
df.to_csv("weather_data.csv", index=False)
print("Dữ liệu đã được lưu vào weather_data.csv")
