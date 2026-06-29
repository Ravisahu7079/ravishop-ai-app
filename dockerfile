# Base image — Python 3.11 slim (lightweight)
FROM python:3.11-slim

# Kyu slim? — Chota image = fast deploy = less cost

# Working directory set karo container ke andar
WORKDIR /app

# Pehle requirements copy karo (cache optimization)
COPY requirements.txt .

# Packages install karo
RUN pip install --no-cache-dir -r requirements.txt

# Baaki sab code copy karo
COPY . .

# Port expose karo
EXPOSE 5000

# App run karo
CMD ["python", "app.py"]
