# 1. Usar una imagen base de Node.js ligera
FROM node:20-slim

# 2. Instalar Python 3, FFmpeg y herramientas necesarias en el servidor
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Crear y pararse en la carpeta de trabajo dentro del servidor
WORKDIR /app

# 4. Copiar e instalar dependencias de Node.js
COPY package*.json ./
RUN npm install

# 5. Copiar e instalar dependencias de Python
COPY requirements.txt ./
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# 6. Copiar absolutamente todo el resto de tu código al servidor
COPY . .

# 7. Comando definitivo para encender tu bot de WhatsApp
CMD ["npm", "start"]