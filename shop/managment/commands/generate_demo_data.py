import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.utils import timezone

from shop.models import Category, Order, OrderItem, Product

User = get_user_model()


class Command(BaseCommand):
    help = "Генерирует демонстрационные данные для проекта"

    def add_arguments(self, parser):
        parser.add_argument(
            "--orders", type=int, default=50, help="Количество заказов для создания"
        )
        parser.add_argument(
            "--products", type=int, default=30, help="Количество товаров для создания"
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Генерация демонстрационных данных..."))

        # Создаем дополнительные категории
        categories_data = [
            {
                "name": "Мужская одежда",
                "slug": "mens-clothing",
                "description": "Стильная мужская одежда",
            },
            {
                "name": "Женская одежда",
                "slug": "womens-clothing",
                "description": "Модная женская одежда",
            },
            {"name": "Обувь", "slug": "shoes", "description": "Качественная обувь"},
            {
                "name": "Аксессуары",
                "slug": "accessories",
                "description": "Стильные аксессуары",
            },
            {
                "name": "Спортивная одежда",
                "slug": "sportswear",
                "description": "Одежда для спорта",
            },
            {
                "name": "Детская одежда",
                "slug": "kids-clothing",
                "description": "Одежда для детей",
            },
            {
                "name": "Нижнее белье",
                "slug": "underwear",
                "description": "Комфортное нижнее белье",
            },
            {
                "name": "Верхняя одежда",
                "slug": "outerwear",
                "description": "Куртки и пальто",
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            if created:
                self.stdout.write(f"✅ Создана категория: {category.name}")

        # Создаем дополнительных пользователей
        customers_data = [
            {
                "username": "anna_smith",
                "first_name": "Анна",
                "last_name": "Смирнова",
                "email": "anna@example.com",
            },
            {
                "username": "ivan_petrov",
                "first_name": "Иван",
                "last_name": "Петров",
                "email": "ivan@example.com",
            },
            {
                "username": "maria_jones",
                "first_name": "Мария",
                "last_name": "Джонс",
                "email": "maria@example.com",
            },
            {
                "username": "alex_brown",
                "first_name": "Алексей",
                "last_name": "Браун",
                "email": "alex@example.com",
            },
            {
                "username": "elena_white",
                "first_name": "Елена",
                "last_name": "Уайт",
                "email": "elena@example.com",
            },
        ]

        for customer_data in customers_data:
            user, created = User.objects.get_or_create(
                username=customer_data["username"],
                defaults={**customer_data, "role": "customer"},
            )
            if created:
                user.set_password("demo123")
                user.save()
                self.stdout.write(f"✅ Создан покупатель: {user.username}")

        # Создаем товары
        products_data = [
            # Мужская одежда
            {
                "name": "Классическая рубашка",
                "category": "mens-clothing",
                "price": 2500,
                "description": "Элегантная мужская рубашка из хлопка",
            },
            {
                "name": "Деловой костюм",
                "category": "mens-clothing",
                "price": 15000,
                "description": "Стильный деловой костюм",
            },
            {
                "name": "Джинсы классические",
                "category": "mens-clothing",
                "price": 3500,
                "description": "Удобные мужские джинсы",
            },
            {
                "name": "Поло рубашка",
                "category": "mens-clothing",
                "price": 1800,
                "description": "Спортивная поло рубашка",
            },
            # Женская одежда
            {
                "name": "Летнее платье",
                "category": "womens-clothing",
                "price": 4500,
                "description": "Легкое летнее платье",
            },
            {
                "name": "Деловая блузка",
                "category": "womens-clothing",
                "price": 2800,
                "description": "Элегантная блузка для офиса",
            },
            {
                "name": "Джинсы скинни",
                "category": "womens-clothing",
                "price": 3200,
                "description": "Модные женские джинсы",
            },
            {
                "name": "Вечернее платье",
                "category": "womens-clothing",
                "price": 8500,
                "description": "Роскошное вечернее платье",
            },
            # Обувь
            {
                "name": "Кроссовки Nike",
                "category": "shoes",
                "price": 6500,
                "description": "Спортивные кроссовки Nike",
            },
            {
                "name": "Туфли классические",
                "category": "shoes",
                "price": 4200,
                "description": "Классические кожаные туфли",
            },
            {
                "name": "Ботинки зимние",
                "category": "shoes",
                "price": 5800,
                "description": "Теплые зимние ботинки",
            },
            {
                "name": "Сандалии летние",
                "category": "shoes",
                "price": 2200,
                "description": "Удобные летние сандалии",
            },
            # Аксессуары
            {
                "name": "Кожаный ремень",
                "category": "accessories",
                "price": 1500,
                "description": "Стильный кожаный ремень",
            },
            {
                "name": "Наручные часы",
                "category": "accessories",
                "price": 12000,
                "description": "Элегантные наручные часы",
            },
            {
                "name": "Кошелек кожаный",
                "category": "accessories",
                "price": 2800,
                "description": "Качественный кожаный кошелек",
            },
            {
                "name": "Солнцезащитные очки",
                "category": "accessories",
                "price": 3500,
                "description": "Модные солнцезащитные очки",
            },
            # Спортивная одежда
            {
                "name": "Спортивный костюм",
                "category": "sportswear",
                "price": 4500,
                "description": "Удобный спортивный костюм",
            },
            {
                "name": "Футболка для бега",
                "category": "sportswear",
                "price": 1200,
                "description": "Дышащая футболка для спорта",
            },
            {
                "name": "Леггинсы для йоги",
                "category": "sportswear",
                "price": 2200,
                "description": "Эластичные леггинсы",
            },
            {
                "name": "Толстовка с капюшоном",
                "category": "sportswear",
                "price": 3200,
                "description": "Теплая спортивная толстовка",
            },
        ]

        for i, prod_data in enumerate(products_data[: options["products"]]):
            try:
                category = Category.objects.get(slug=prod_data["category"])
                product, created = Product.objects.get_or_create(
                    slug=f"{prod_data['category']}-{i + 1}",
                    defaults={
                        "name": prod_data["name"],
                        "category": category,
                        "description": prod_data["description"],
                        "price": Decimal(str(prod_data["price"])),
                        "stock": random.randint(5, 50),
                        "available": True,
                    },
                )
                if created:
                    self.stdout.write(f"✅ Создан товар: {product.name}")
            except Category.DoesNotExist:
                self.stdout.write(f'❌ Категория {prod_data["category"]} не найдена')

        # Создаем заказы
        customers = User.objects.filter(role="customer")
        products = Product.objects.filter(available=True)

        if not customers.exists() or not products.exists():
            self.stdout.write(
                self.style.ERROR("❌ Недостаточно данных для создания заказов")
            )
            return

        statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

        for i in range(options["orders"]):
            # Случайная дата в последние 60 дней
            days_ago = random.randint(0, 60)
            order_date = timezone.now() - timedelta(days=days_ago)

            customer = random.choice(customers)

            order = Order.objects.create(
                user=customer,
                first_name=customer.first_name or "Имя",
                last_name=customer.last_name or "Фамилия",
                email=customer.email,
                phone=f"+7{random.randint(9000000000, 9999999999)}",
                address=f"ул. Примерная, д. {random.randint(1, 100)}",
                city="Москва",
                postal_code=f"{random.randint(100000, 199999)}",
                status=random.choice(statuses),
                created_at=order_date,
                total_price=0,  # Будет пересчитано ниже
            )

            # Добавляем товары в заказ
            num_items = random.randint(1, 5)
            total_price = Decimal("0")

            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price

                OrderItem.objects.create(
                    order=order, product=product, price=price, quantity=quantity
                )

                total_price += price * quantity

            order.total_price = total_price
            order.save()

            if i % 10 == 0:
                self.stdout.write(f'📦 Создано заказов: {i + 1}/{options["orders"]}')

        # Статистика
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_customers = User.objects.filter(role="customer").count()
        total_revenue = Order.objects.aggregate(total=Sum("total_price"))["total"] or 0

        self.stdout.write(self.style.SUCCESS("\n🎉 Генерация данных завершена!"))
        self.stdout.write("📊 Статистика:")
        self.stdout.write(f"   👥 Покупателей: {total_customers}")
        self.stdout.write(f"   📦 Товаров: {total_products}")
        self.stdout.write(f"   🛒 Заказов: {total_orders}")
        self.stdout.write(f"   💰 Общая выручка: {total_revenue} ₽")

        self.stdout.write(
            self.style.SUCCESS(
                "\n✨ Теперь можно протестировать dashboard с реальными данными!"
            )
        )
