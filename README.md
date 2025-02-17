# Weather ETL Project

## 1️⃣ Giới thiệu
Dự án **Weather ETL** sử dụng **Apache Spark** để xử lý và lưu trữ dữ liệu thời tiết vào **PostgreSQL**. Dữ liệu được lấy từ một tập tin CSV hoặc có thể mở rộng để lấy từ API thời tiết.

Dự án bao gồm:
- **Docker Compose** để chạy Spark và PostgreSQL.
- **ETL Pipeline** để đọc, xử lý và lưu dữ liệu vào PostgreSQL.
- **Phân cụm dữ liệu thời tiết bằng K-Means** với Spark MLlib.

---

## 2️⃣ Cách cài đặt và chạy dự án

### **Bước 1: Cài đặt môi trường Docker và PySpark**

1. **Tạo và kích hoạt virtual environment (nếu cần)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Chạy Docker Compose để khởi động Spark và PostgreSQL**:
   ```bash
   docker-compose up -d
   ```

3. **Cài đặt PySpark trong container**:
   ```bash
   docker exec -it spark-master bash
   pip install pyspark
   exit
   ```

---

### **Bước 2: Chuẩn bị dữ liệu**
1. **Kiểm tra tập tin dữ liệu CSV có tồn tại không**:
   ```python
   import os
   csv_path = "/opt/bitnami/spark/weather_data.csv"
   if not os.path.exists(csv_path):
       print(f"❌ File không tồn tại: {csv_path}")
   ```
2. **Copy file CSV vào container**:
   ```bash
   docker cp weather_data.csv spark-master:/opt/bitnami/spark/weather_data.csv
   ```
3. **Kiểm tra file trong container**:
   ```bash
   docker exec -it spark-master ls /opt/bitnami/spark
   ```

---

### **Bước 3: Cấu hình Spark để kết nối PostgreSQL**
1. **Cài đặt JDBC driver trong container**:
   ```bash
   curl -o postgresql-42.2.20.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.20.jar
   docker cp postgresql-42.2.20.jar spark-master:/opt/bitnami/spark/jars/
   ```
2. **Xác minh driver đã được thêm vào Spark**:
   ```bash
   docker exec -it spark-master ls -l /opt/bitnami/spark/jars/postgresql-42.2.20.jar
   ```

---

### **Bước 4: Chạy script ETL để xử lý dữ liệu**
1. **Copy script ETL vào container**:
   ```bash
   docker cp weather_etl.py spark-master:/weather_etl.py
   ```
2. **Chạy Spark script trong container**:
   ```bash
   docker exec -it spark-master bash -c "spark-submit /weather_etl.py"
   ```

---

### **Bước 5: Kiểm tra dữ liệu trong PostgreSQL**
1. **Kiểm tra kết nối PostgreSQL**:
   ```bash
   docker exec -it postgres-db psql -U admin -d weather_db -c "SELECT 1;"
   ```
2. **Xem danh sách các bảng trong PostgreSQL**:
   ```sql
   SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
   ```
3. **Kiểm tra dữ liệu trong bảng `weather`**:
   ```sql
   SELECT * FROM weather LIMIT 5;
   ```

---

## 3️⃣ Lỗi thường gặp và cách khắc phục

### ❌ **1. Lỗi Py4J: Không tìm thấy JDBC driver**
**Cách khắc phục:** Đảm bảo đã tải về **postgresql-42.2.20.jar** và copy vào đúng thư mục:
```bash
docker cp postgresql-42.2.20.jar spark-master:/opt/bitnami/spark/jars/
```

### ❌ **2. Lỗi kết nối PostgreSQL: `password authentication failed`**
**Cách khắc phục:**
- Kiểm tra lại tài khoản PostgreSQL:
  ```bash
  docker exec -it postgres-db psql -U admin -d postgres
  SELECT usename FROM pg_user;
  ```
- Đảm bảo URL kết nối đúng trong `weather_etl.py`:
  ```python
  postgres_url = "jdbc:postgresql://postgres-db:5432/weather_db"
  postgres_properties = {
      "user": "admin",
      "password": "123456",
      "driver": "org.postgresql.Driver"
  }
  ```

### ❌ **3. Lỗi file CSV không tồn tại**
**Cách khắc phục:** Copy lại file vào container:
```bash
docker cp weather_data.csv spark-master:/opt/bitnami/spark/weather_data.csv
```

### ❌ **4. Lỗi bảng không tồn tại trong PostgreSQL**
**Cách khắc phục:** Kiểm tra xem bảng đã được tạo chưa:
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```
Nếu không có bảng `weather`, chạy lại ETL script.

### ❌ **5. Dữ liệu NULL sau khi chuyển đổi**
**Cách khắc phục:**
- Kiểm tra dữ liệu gốc từ CSV:
  ```bash
  docker exec -it spark-master bash -c "cat /opt/bitnami/spark/weather_data.csv"
  ```
- Kiểm tra schema sau khi đọc:
  ```python
  df.printSchema()
  ```

---

## 4️⃣ Tích hợp Phân Cụm Dữ Liệu với Spark MLlib
Sau khi ETL xong, ta có thể phân cụm dữ liệu bằng **K-Means Clustering** để tìm **các nhóm thời tiết tương tự nhau**.

### **📌 Bước 1: Chạy script phân cụm**
```bash
docker exec -it spark-master bash -c "spark-submit /weather_clustering.py"
```

### **📌 Bước 2: Kiểm tra kết quả phân cụm**
```sql
SELECT * FROM weather_clusters;
```
Bảng sẽ chứa cột `prediction`, cho biết mỗi bản ghi thuộc cụm nào.

---

## 5️⃣ Tổng kết
- **Docker giúp dễ dàng triển khai Spark và PostgreSQL** mà không cần cài đặt nhiều.
- **Spark giúp xử lý dữ liệu lớn và chạy mô hình machine learning**.
- **PostgreSQL là nơi lưu trữ dữ liệu** để dễ dàng truy vấn và phân tích.

Dự án này có thể mở rộng bằng cách:
- **Thu thập dữ liệu tự động từ API** thay vì CSV.
- **Dự báo xu hướng thời tiết** bằng các mô hình machine learning khác.

🔥 **Chạy thử ngay và mở rộng dự án của bạn!** 🚀

