# Gunakan gambar dasar dari Python versi terbaru
FROM python:3.9-slim

# Atur direktori kerja
WORKDIR /main

# Salin file requirements.txt ke dalam image
COPY requirements.txt .

# Instal dependensi yang diperlukan
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari direktori lokal ke dalam image
COPY . .

# Tentukan variabel lingkungan
ENV API_TOKEN=$API_TOKEN

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "main.py"]
