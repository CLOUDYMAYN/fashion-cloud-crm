import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from shop.models import Order, OrderItem, Product

User = get_user_model()


class Command(BaseCommand):
    help = "Настройка аналитических данных для демонстрации"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔧 Настройка аналитических данных..."))

        # Создаем дополнительные заказы для лучшей аналитики
        self.create_analytical_orders()

        # Обновляем остатки товаров для демонстрации уведомлений
        self.update_stock_levels()

        self.stdout.write(self.style.SUCCESS("✅ Аналитические данные настроены!"))

    def create_analytical_orders(self):
        """Создает заказы с различными паттернами для аналитики"""
        customers = User.objects.filter(role="customer")
        products = Product.objects.filter(available=True)

        if not customers.exists() or not products.exists():
            self.stdout.write(self.style.WARNING("⚠️ Недостаточно данных для создания заказов"))
            return

        # Создаем заказы за последние 90 дней с различными трендами
        for days_ago in range(90):
            date = timezone.now() - timedelta(days=days_ago)

            # Больше заказов в выходные и праздники
            orders_count = random.randint(2, 8)
            if date.weekday() >= 5:  # Выходные
                orders_count = random.randint(5, 12)

            for _ in range(orders_count):
                customer = random.choice(customers)

                order = Order.objects.create(
                    user=customer,
                    first_name=customer.first_name or f"Покупатель{random.randint(1, 100)}",
                    last_name=customer.last_name or f"Тестовый{random.randint(1, 100)}",
                    email=customer.email or f"test{random.randint(1, 1000)}@example.com",
                    phone=f"+7{random.randint(9000000000, 9999999999)}",
                    address=f"ул. Тестовая, д. {random.randint(1, 100)}",
                    city="Москва",
                    postal_code=f"{random.randint(100000, 199999)}",
                    status=random.choices(
                        ["pending", "processing", "shipped", "delivered", "cancelled"],
                        weights=[10, 20, 15, 50, 5],  # Больше доставленных заказов
                    )[0],
                    created_at=date,
                    total_price=0,
                )

                # Добавляем товары в заказ
                num_items = random.randint(1, 4)
                total_price = Decimal("0")

                selected_products = random.sample(list(products), min(num_items, len(products)))

                for product in selected_products:
                    quantity = random.randint(1, 3)
                    price = product.price

                    OrderItem.objects.create(
                        order=order, product=product, price=price, quantity=quantity
                    )

                    total_price += price * quantity

                order.total_price = total_price
                order.save()

        self.stdout.write("📊 Создано дополнительных заказов для аналитики")

    def update_stock_levels(self):
        """Обновляет остатки товаров для демонстрации уведомлений"""
        products = Product.objects.all()

        # Делаем несколько товаров с низким остатком
        low_stock_products = random.sample(list(products), min(5, len(products)))

        for product in low_stock_products:
            product.stock = random.randint(1, 4)  # Низкий остаток
            product.save()
            self.stdout.write(f'⚠️ Товар "{product.name}" - остаток: {product.stock}')

        # Остальные товары с нормальным остатком
        for product in products:
            if product not in low_stock_products:
                product.stock = random.randint(10, 50)
                product.save()
