#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Настройка демонстрационного окружения...${NC}"

# Проверяем, что мы в правильной директории
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Файл manage.py не найден. Убедитесь, что вы в корневой директории проекта.${NC}"
    exit 1
fi

# Активируем виртуальное окружение если оно существует
if [ -d "venv" ]; then
    echo -e "${YELLOW}📦 Активация виртуального окружения...${NC}"
    source venv/bin/activate
fi

# Устанавливаем зависимости
echo -e "${YELLOW}📥 Установка зависимостей...${NC}"
pip install -r requirements.txt

# Применяем миграции
echo -e "${YELLOW}🔄 Применение миграций...${NC}"
python manage.py migrate

# Создаем базовых пользователей
echo -e "${YELLOW}👥 Создание тестовых пользователей...${NC}"
python manage.py create_test_users

# Генерируем демонстрационные данные
echo -e "${YELLOW}📊 Генерация демонстрационных данных...${NC}"
python manage.py generate_demo_data --orders 100 --products 50

# Собираем статические файлы
echo -e "${YELLOW}📁 Сбор статических файлов...${NC}"
python manage.py collectstatic --noinput

# Создаем суперпользователя если нужно
echo -e "${YELLOW}👑 Создание суперпользователя...${NC}"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fashionstore.com', 'admin123')
    print('Суперпользователь создан: admin / admin123')
else:
    print('Суперпользователь уже существует')
EOF

# Генерируем аналитический отчет
echo -e "${YELLOW}📈 Генерация аналитического отчета...${NC}"
python manage.py analytics_report --days 30 > analytics_report.txt

echo -e "${GREEN}✅ Демонстрационное окружение настроено!${NC}"
echo -e "${BLUE}📋 Доступные аккаунты:${NC}"
echo -e "   👑 Суперпользователь: admin / admin123"
echo -e "   🏆 Босс: boss / boss123"
echo -e "   👔 Менеджер: manager / manager123"
echo -e "   👤 Покупатель: customer / customer123"

echo -e "${BLUE}🌐 Запуск сервера:${NC}"
echo -e "   python manage.py runserver"

echo -e "${BLUE}📊 Полезные команды:${NC}"
echo -e "   python manage.py analytics_report --days 7"
echo -e "   python manage.py generate_demo_data --orders 50"
echo -e "   python manage.py shell"

echo -e "${GREEN}🎉 Готово! Можно начинать демонстрацию.${NC}"
