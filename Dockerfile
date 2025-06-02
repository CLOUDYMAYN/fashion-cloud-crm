FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копирование виртуального окружения из builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создание пользователя для безопасности
RUN groupadd -r django && useradd -r -g django django

# Создание рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

# Переключение на непривилегированного пользователя
USER django

# Открытие порта
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "crm_shop.wsgi:application"]


ENV DJANGO_SETTINGS_MODULE=crm_shop.settings.production
ENV SECRET_KEY=your-secret-key
ENV DEBUG=False



