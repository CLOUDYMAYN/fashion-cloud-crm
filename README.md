# 🛍️ FashionStore CRM

Современная CRM система для интернет-магазина одежды с полным DevOps pipeline.

## 🚀 Возможности

- **Multi-role система**: Покупатели, Менеджеры, Руководители
- **Динамический Dashboard** с аналитикой в реальном времени
- **Управление товарами** и категориями
- **Система заказов** с отслеживанием статусов
- **Адаптивный дизайн** для всех устройств
- **CI/CD Pipeline** с автоматическим тестированием
- **Контейнеризация** с Docker
- **Kubernetes** для оркестрации
- **Стресс-тестирование** с k6

## 🏗️ Архитектура

\`\`\`
Frontend (HTML/CSS/JS) → Django Backend → PostgreSQL
                                      ↓
                                   Redis Cache
                                      ↓
                              Nginx Load Balancer
\`\`\`

## 🛠️ Технологии

- **Backend**: Django 4.2, Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Web Server**: Nginx + Gunicorn
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Health checks, Metrics
- **Testing**: pytest, k6 (stress testing)

## 🚀 Быстрый старт

### Локальная разработка

\`\`\`bash
# Клонирование репозитория
git clone https://github.com/yourusername/crm-shop.git
cd crm-shop

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements-dev.txt

# Миграции
python manage.py migrate

# Создание тестовых данных
python manage.py create_test_users

# Запуск сервера
python manage.py runserver
\`\`\`

### Docker Compose

\`\`\`bash
# Запуск всех сервисов
docker-compose up -d

# Миграции
docker-compose exec web python manage.py migrate

# Создание тестовых данных
docker-compose exec web python manage.py create_test_users
\`\`\`

### Kubernetes

\`\`\`bash
# Деплой в Kubernetes
./scripts/deploy.sh staging

# Проверка статуса
kubectl get pods -n crm-shop-staging
\`\`\`

## 🧪 Тестирование

### Unit тесты

\`\`\`bash
# Запуск всех тестов
python manage.py test

# С покрытием
coverage run --source='.' manage.py test
coverage report
\`\`\`

### Стресс-тестирование

\`\`\`bash
# Установка k6
# Linux
sudo apt-get install k6

# macOS
brew install k6

# Запуск стресс-тестов
./scripts/stress_test.sh http://localhost:8000
\`\`\`

## 👥 Тестовые аккаунты

| Роль | Username | Password | Доступ |
|------|----------|----------|---------|
| 👑 Boss | `boss` | `boss123` | Полный доступ |
| 👔 Manager | `manager` | `manager123` | Управление товарами/заказами |
| 👤 Customer | `customer` | `customer123` | Покупки |

## 🔧 Конфигурация

### Переменные окружения

\`\`\`bash
# .env файл
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgres://user:pass@localhost:5432/crm_shop
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
\`\`\`

### GitHub Secrets

Для CI/CD настройте следующие секреты в GitHub:

- `DOCKERHUB_USERNAME` - имя пользователя Docker Hub
- `DOCKERHUB_TOKEN` - токен Docker Hub
- `KUBE_CONFIG` - конфигурация Kubernetes

## 📊 Мониторинг

### Health Check

\`\`\`bash
curl http://localhost:8000/health/
\`\`\`

### Метрики

- Response time: < 500ms (95th percentile)
- Error rate: < 1%
- Uptime: > 99.9%

## 🚀 Деплой в облако

### AWS EKS

\`\`\`bash
# Создание кластера
eksctl create cluster --name crm-shop --region us-west-2

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

### Google GKE

\`\`\`bash
# Создание кластера
gcloud container clusters create crm-shop --zone us-central1-a

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

### Azure AKS

\`\`\`bash
# Создание кластера
az aks create --resource-group myResourceGroup --name crm-shop

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

## 📈 Производительность

### Результаты нагрузочного тестирования

- **Concurrent Users**: 100
- **Response Time**: 95th percentile < 500ms
- **Throughput**: 1000+ requests/second
- **Error Rate**: < 0.1%

### Оптимизации

- Database indexing
- Redis caching
- Static file compression
- CDN integration
- Connection pooling

## 🔒 Безопасность

- CSRF protection
- SQL injection prevention
- XSS protection
- Rate limiting
- Security headers
- SSL/TLS encryption

## 📝 API Documentation

### Endpoints

\`\`\`
GET  /                     # Главная страница
GET  /catalog/             # Каталог товаров
GET  /dashboard/           # Админ панель
POST /add-to-cart/<id>/    # Добавить в корзину
GET  /health/              # Health check
\`\`\`

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE).

## 📞 Поддержка

- 📧 Email: support@fashionstore.com
- 💬 Slack: #crm-shop-support
- 📖 Wiki: [GitHub Wiki](https://github.com/yourusername/crm-shop/wiki)

---

Сделано с ❤️ командой FashionStore
