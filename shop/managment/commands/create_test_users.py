# from django.contrib.auth import get_user_model
# from django.core.management.base import BaseCommand
#
# from shop.models import Category, Product
#
# User = get_user_model()
#
#
# class Command(BaseCommand):
#     help = "Создает тестовых пользователей и данные"
#
#     def handle(self, *args, **options):
#         boss, created = User.objects.get_or_create(
#             username="boss",
#             defaults={
#                 "email": "boss@fashionstore.ru",
#                 "first_name": "Иван",
#                 "last_name": "Петров",
#                 "role": "boss",
#                 "is_staff": True,
#                 "is_superuser": True,
#             },
#         )
#         if created:
#             boss.set_password("boss123")
#             boss.save()
#             self.stdout.write(self.style.SUCCESS("Создан босс: username=boss, password=boss123"))
#         else:
#             self.stdout.write(f"Босс уже существует: {boss.username}")
#
#         # Создаем менеджера
#         manager, created = User.objects.get_or_create(
#             username="manager",
#             defaults={
#                 "email": "manager@fashionstore.ru",
#                 "first_name": "Анна",
#                 "last_name": "Сидорова",
#                 "role": "manager",
#                 "is_staff": True,
#             },
#         )
#         if created:
#             manager.set_password("manager123")
#             manager.save()
#             self.stdout.write(
#                 self.style.SUCCESS("Создан менеджер: username=manager, password=manager123")
#             )
#         else:
#             self.stdout.write(f"Менеджер уже существует: {manager.username}")
#
#         # Создаем тестового покупателя
#         customer, created = User.objects.get_or_create(
#             username="customer",
#             defaults={
#                 "email": "customer@example.com",
#                 "first_name": "Мария",
#                 "last_name": "Иванова",
#                 "role": "customer",
#             },
#         )
#         if created:
#             customer.set_password("customer123")
#             customer.save()
#             self.stdout.write(
#                 self.style.SUCCESS("Создан покупатель: username=customer, password=customer123")
#             )
#         else:
#             self.stdout.write(f"Покупатель уже существует: {customer.username}")
#
#         # Создаем категории
#         categories_data = [
#             {
#                 "name": "Мужская одежда",
#                 "slug": "mens-clothing",
#                 "description": "Стильная мужская одежда",
#             },
#             {
#                 "name": "Женская одежда",
#                 "slug": "womens-clothing",
#                 "description": "Модная женская одежда",
#             },
#             {"name": "Обувь", "slug": "shoes", "description": "Качественная обувь"},
#             {
#                 "name": "Аксессуары",
#                 "slug": "accessories",
#                 "description": "Стильные аксессуары",
#             },
#         ]
#
#         for cat_data in categories_data:
#             category, created = Category.objects.get_or_create(
#                 slug=cat_data["slug"], defaults=cat_data
#             )
#             if created:
#                 self.stdout.write(f"Создана категория: {category.name}")
#
#         # Создаем тестовые товары
#         if Category.objects.exists():
#             mens_category = Category.objects.get(slug="mens-clothing")
#             womens_category = Category.objects.get(slug="womens-clothing")
#
#             products_data = [
#                 {
#                     "name": "Мужская рубашка",
#                     "slug": "mens-shirt",
#                     "category": mens_category,
#                     "description": "Классическая мужская рубашка из хлопка",
#                     "price": 2500,
#                     "stock": 10,
#                 },
#                 {
#                     "name": "Женское платье",
#                     "slug": "womens-dress",
#                     "category": womens_category,
#                     "description": "Элегантное женское платье",
#                     "price": 4500,
#                     "stock": 5,
#                 },
#                 {
#                     "name": "Мужские джинсы",
#                     "slug": "mens-jeans",
#                     "category": mens_category,
#                     "description": "Стильные мужские джинсы",
#                     "price": 3500,
#                     "stock": 8,
#                 },
#                 {
#                     "name": "Женская блузка",
#                     "slug": "womens-blouse",
#                     "category": womens_category,
#                     "description": "Легкая женская блузка",
#                     "price": 2000,
#                     "stock": 12,
#                 },
#             ]
#
#             for prod_data in products_data:
#                 product, created = Product.objects.get_or_create(
#                     slug=prod_data["slug"], defaults=prod_data
#                 )
#                 if created:
#                     self.stdout.write(f"Создан товар: {product.name}")
#
#         self.stdout.write(self.style.SUCCESS("\n=== ГОТОВЫЕ АККАУНТЫ ==="))
#         self.stdout.write("Босс: username=boss, password=boss123")
#         self.stdout.write("Менеджер: username=manager, password=manager123")
#         self.stdout.write("Покупатель: username=customer, password=customer123")
#         self.stdout.write("\nДля входа в админку используйте аккаунт босса или менеджера")
