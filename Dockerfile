# استفاده از تصویر رسمی پایتون
FROM python:3.11-slim

# تنظیم متغیرهای محیطی پایتون
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعیین دایرکتوری کاری
WORKDIR /app

# نصب پیش‌نیازهای سیستمی
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل نیازمندی‌ها و نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی تمام فایل‌های پروژه
COPY . .

# اجرای ربات
CMD ["python", "main.py"]
