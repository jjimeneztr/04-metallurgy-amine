# Utilizar una imagen base oficial de Python
FROM python:3.11

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Definir el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
