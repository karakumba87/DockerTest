# Используйте официальный образ Python
FROM python:3.8

# Установите зависимости
RUN pip install psycopg2-binary flask

# Копируйте код приложения в контейнер
COPY . /app
WORKDIR /app

# Укажите, как запустить приложение
CMD ["python", "app.py"]
