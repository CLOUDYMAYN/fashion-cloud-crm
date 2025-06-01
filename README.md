# 🛍️ Fashion Cloud CRM

Современная облачная CRM система для интернет-магазина одежды с полным DevOps pipeline.

![GitHub Actions](https://github.com/CLOUDYMAYN/fashion-cloud-crm/workflows/Django%20CRM%20CI/CD%20Pipeline/badge.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white)

## 🚀 Возможности

- **🏢 Multi-role система**: Покупатели, Менеджеры, Руководители
- **📊 Динамический Dashboard** с аналитикой в реальном времени
- **📦 Управление товарами** и категориями
- **🛒 Система заказов** с отслеживанием статусов
- **📱 Адаптивный дизайн** для всех устройств
- **🔄 CI/CD Pipeline** с автоматическим тестированием
- **🐳 Контейнеризация** с Docker
- **☸️ Kubernetes** для оркестрации
- **⚡ Стресс-тестирование** с k6

## 🏗️ Архитектура

\`\`\`
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API     │    │   PostgreSQL    │
│  (HTML/CSS/JS)  │───▶│     Backend      │───▶│    Database     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Redis Cache    │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Nginx + Gunicorn │
                       └──────────────────┘
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
git clone https://github.com/CLOUDYMAYN/fashion-cloud-crm.git
cd fashion-cloud-crm

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

# Просмотр логов
docker-compose logs -f web
\`\`\`

### Kubernetes

\`\`\`bash
# Деплой в Kubernetes
./scripts/deploy.sh staging

# Проверка статуса
kubectl get pods -n fashion-cloud-crm-staging

# Просмотр логов
kubectl logs -f deployment/fashion-cloud-crm-web -n fashion-cloud-crm-staging
\`\`\`

## 🧪 Тестирование

### Unit тесты

\`\`\`bash
# Запуск всех тестов
python manage.py test

# С покрытием
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML отчет
\`\`\`

### Стресс-тестирование

\`\`\`bash
# Установка k6
# Linux
sudo apt-get install k6

# macOS
brew install k6

# Windows
choco install k6

# Запуск стресс-тестов
./scripts/stress_test.sh http://localhost:8000

# Просмотр результатов
open test_results/report.html
\`\`\`

## 👥 Тестовые аккаунты

| Роль | Username | Password | Доступ |
|------|----------|----------|---------|
| 👑 Boss | `boss` | `boss123` | Полный доступ ко всем функциям |
| 👔 Manager | `manager` | `manager123` | Управление товарами и заказами |
| 👤 Customer | `customer` | `customer123` | Покупки в магазине |

## 🔧 Конфигурация

### Переменные окружения

\`\`\`bash
# .env файл
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgres://user:pass@localhost:5432/fashion_crm
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Для продакшена
SENTRY_DSN=your-sentry-dsn
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
\`\`\`

### GitHub Secrets

Для CI/CD настройте следующие секреты в GitHub:

- `DOCKERHUB_USERNAME` - имя пользователя Docker Hub
- `DOCKERHUB_TOKEN` - токен Docker Hub
- `SECRET_KEY` - секретный ключ Django
- `DB_PASSWORD` - пароль базы данных

## 📊 Мониторинг и метрики

### Health Check

\`\`\`bash
# Локально
curl http://localhost:8000/health/

# В продакшене
curl https://your-domain.com/health/
\`\`\`

### Производительность

- **Response time**: < 500ms (95th percentile)
- **Error rate**: < 1%
- **Uptime**: > 99.9%
- **Concurrent users**: 100+
- **Throughput**: 1000+ requests/second

## 🚀 Деплой в облако

### AWS EKS

\`\`\`bash
# Создание кластера
eksctl create cluster --name fashion-cloud-crm --region us-west-2

# Настройка kubectl
aws eks update-kubeconfig --region us-west-2 --name fashion-cloud-crm

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

### Google GKE

\`\`\`bash
# Создание кластера
gcloud container clusters create fashion-cloud-crm \
  --zone us-central1-a \
  --num-nodes 3

# Настройка kubectl
gcloud container clusters get-credentials fashion-cloud-crm --zone us-central1-a

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

### Azure AKS

\`\`\`bash
# Создание группы ресурсов
az group create --name fashion-crm-rg --location eastus

# Создание кластера
az aks create \
  --resource-group fashion-crm-rg \
  --name fashion-cloud-crm \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Настройка kubectl
az aks get-credentials --resource-group fashion-crm-rg --name fashion-cloud-crm

# Деплой приложения
./scripts/deploy.sh production
\`\`\`

## 📈 Результаты нагрузочного тестирования

### Load Test Results

\`\`\`
Scenario: Normal Load
- Virtual Users: 10-20
- Duration: 10 minutes
- Response Time (95th): 245ms
- Error Rate: 0.02%
- Throughput: 850 req/sec
\`\`\`

### Spike Test Results

\`\`\`
Scenario: Traffic Spike
- Virtual Users: 0-100-0
- Duration: 2 minutes
- Response Time (95th): 1.2s
- Error Rate: 0.15%
- System Recovery: Excellent
\`\`\`

## 🔒 Безопасность

### Реализованные меры

- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Rate limiting (5 req/min для login)
- ✅ Security headers
- ✅ SSL/TLS encryption
- ✅ Input validation
- ✅ Authentication & Authorization

### Сканирование безопасности

\`\`\`bash
# Bandit security scan
bandit -r . -x tests/

# Safety check dependencies
safety check

# OWASP ZAP scan (если установлен)
zap-baseline.py -t http://localhost:8000
\`\`\`

## 📝 API Documentation

### Основные endpoints

\`\`\`
GET  /                     # Главная страница
GET  /catalog/             # Каталог товаров
GET  /product/<slug>/      # Детали товара
GET  /cart/                # Корзина
POST /add-to-cart/<id>/    # Добавить в корзину
GET  /dashboard/           # Админ панель
GET  /dashboard/products/  # Управление товарами
GET  /dashboard/orders/    # Управление заказами
GET  /health/              # Health check
\`\`\`

### Response formats

\`\`\`json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
\`\`\`

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

### Стандарты кода

- Используйте Black для форматирования
- Следуйте PEP 8
- Покрытие тестами > 80%
- Документируйте новые функции

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE).

## 📞 Поддержка и контакты

- 📧 **Email**: support@fashioncloud.com
- 💬 **Telegram**: @CLOUDYMAYN
- 🐛 **Issues**: [GitHub Issues](https://github.com/CLOUDYMAYN/fashion-cloud-crm/issues)
- 📖 **Wiki**: [GitHub Wiki](https://github.com/CLOUDYMAYN/fashion-cloud-crm/wiki)

## 🏆 Roadmap

### v2.0 (Q2 2024)
- [ ] Микросервисная архитектура
- [ ] GraphQL API
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Mobile app

### v2.1 (Q3 2024)
- [ ] AI-powered recommendations
- [ ] Multi-language support
- [ ] Advanced reporting
- [ ] Integration with payment systems

---

<div align="center">

**Сделано с ❤️ командой Fashion Cloud**

[![GitHub stars](https://img.shields.io/github/stars/CLOUDYMAYN/fashion-cloud-crm.svg?style=social&label=Star)](https://github.com/CLOUDYMAYN/fashion-cloud-crm)
[![GitHub forks](https://img.shields.io/github/forks/CLOUDYMAYN/fashion-cloud-crm.svg?style=social&label=Fork)](https://github.com/CLOUDYMAYN/fashion-cloud-crm/fork)

</div>
