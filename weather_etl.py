from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, regexp_replace
from sqlalchemy import create_engine, text
import os

# 1️⃣ Khởi tạo SparkSession với driver PostgreSQL
spark = SparkSession.builder \
    .appName("Weather ETL") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.2.20.jar") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

print("✅ SparkSession initialized successfully.")

# 2️⃣ Đọc dữ liệu từ CSV
csv_path = "/opt/bitnami/spark/weather_data.csv"
if not os.path.exists(csv_path):
    print(f"❌ File không tồn tại: {csv_path}")
    exit(1)

df = spark.read.option("header", "true").csv(csv_path)
print(f"✅ Đọc dữ liệu thành công từ {csv_path}. Tổng số dòng: {df.count()}")
df.show()
df.printSchema()

# 3️⃣ Xử lý dữ liệu (Fix lỗi NULL)
weather_df = df.withColumn("date", to_timestamp(col("date"), "yyyy-MM-dd HH:mm:ss")) \
               .withColumn("temperature", regexp_replace(col("temperature"), "\\s*°C", "").cast("float")) \
               .withColumn("humidity", regexp_replace(col("humidity"), "\\s*%", "").cast("float")) \
               .withColumn("wind_speed", regexp_replace(col("wind_speed"), "\\s*km/h", "").cast("float")) 

print("✅ Sau khi chuyển đổi kiểu dữ liệu:")
weather_df.show()
weather_df.printSchema()

# Bước này chỉ giữ lại các dòng hợp lệ
weather_df = weather_df.na.drop()

print(f"✅ Dữ liệu sau khi loại bỏ NULL: {weather_df.count()} dòng")

# 4️⃣ Kết nối đến PostgreSQL
postgres_url = "jdbc:postgresql://postgres-db:5432/weather_db"
postgres_properties = {
    "user": "admin",
    "password": "123456",
    "driver": "org.postgresql.Driver"
}

# 5️⃣ Lưu vào PostgreSQL
try:
    print("✅ Dữ liệu chuẩn bị ghi vào PostgreSQL:")
    weather_df.show()
    
    weather_df.write.jdbc(url=postgres_url, table="weather", mode="overwrite", properties=postgres_properties)
    print("✅ Dữ liệu đã được lưu vào PostgreSQL!")
except Exception as e:
    print(f"❌ Lỗi khi ghi vào PostgreSQL: {e}")
    exit(1)

# 6️⃣ Kiểm tra dữ liệu đã lưu
try:
    engine = create_engine("postgresql://admin:123456@postgres-db:5432/weather_db")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM weather LIMIT 5")).fetchall()
        print("✅ Dữ liệu từ PostgreSQL:")
        for row in result:
            print(row)
except Exception as e:
    print(f"❌ Lỗi khi kiểm tra dữ liệu từ PostgreSQL: {e}")
