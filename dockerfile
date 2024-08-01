FROM python:latest

# Set the working directory
WORKDIR /usr/src/app

# Copia el archivo de requerimientos y el código de la aplicación
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala Puppeteer y Google Chrome
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Instala Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Configura Puppeteer para usar Google Chrome
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

# Expone el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.api.methods:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


