# Используем официальный образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта (main.py и Dockerfile) в контейнер
COPY main.py requirements.txt ./

# Устанавливаем зависимости (если у вас есть дополнительные пакеты)
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт Flask
EXPOSE 5000

# Запускаем сервер Flask
CMD ["python", "main.py"]


# docker build -t flask-analyzer .
# docker run -d -p 5000:5000 flask-analyzer
