import os
from dotenv import load_dotenv


# Инициализация переменных окружения
load_dotenv()

# Инициализация переменных проекта
PROJECT_HOST = os.getenv(
    key="PROJECT_HOST")

PROJECT_PORT = os.getenv(
    key="PROJECT_PORT")

# Адрес базы данных
DATABASE = os.getenv(
    key="DATABASE")
