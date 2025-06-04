# import json
# from datetime import timedelta
#
# from django.core.management.base import BaseCommand
# from django.db.models import Avg, Sum
# from django.utils import timezone
#
# from shop.models import Category, Order, OrderItem, Product, User
#
#
# class Command(BaseCommand):
#     help = "Генерирует аналитический отчет"
#
#     def add_arguments(self, parser):
#         parser.add_argument(
#             "--days",
#             type=int,
#             default=30,
#             help="Количество дней для анализа (по умолчанию 30)",
#         )
#         parser.add_argument(
#             "--format",
#             type=str,
#             choices=["text", "json"],
#             default="text",
#             help="Формат вывода (text или json)",
#         )
#
#     def handle(self, *args, **options):
#         days = options["days"]
#         format_type = options["format"]
#
#         # Период анализа
#         end_date = timezone.now()
#         start_date = end_date - timedelta(days=days)
#
#         # Основная статистика
#         total_orders = Order.objects.filter(created_at__gte=start_date).count()
#         total_revenue = (
#             Order.objects.filter(created_at__gte=start_date).aggregate(total=Sum("total_price"))[
#                 "total"
#             ]
#             or 0
#         )
#
#         avg_order_value = (
#             Order.objects.filter(created_at__gte=start_date).aggregate(avg=Avg("total_price"))[
#                 "avg"
#             ]
#             or 0
#         )
#
#         # Топ товары
#         top_products = (
#             OrderItem.objects.filter(order__created_at__gte=start_date)
#             .values("product__name")
#             .annotate(
#                 total_sold=Sum("quantity"),
#                 total_revenue=Sum("quantity") * Sum("price") / Sum("quantity"),
#             )
#             .order_by("-total_sold")[:10]
#         )
#
#         # Статистика по категориям
#         category_stats = []
#         for category in Category.objects.all():
#             revenue = (
#                 OrderItem.objects.filter(
#                     order__created_at__gte=start_date, product__category=category
#                 ).aggregate(total=Sum("quantity") * Sum("price") / Sum("quantity"))["total"]
#                 or 0
#             )
#
#             category_stats.append({"name": category.name, "revenue": float(revenue)})
#
#         # Статистика по дням
#         daily_stats = []
#         for i in range(days):
#             day = start_date + timedelta(days=i)
#             day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
#             day_end = day_start + timedelta(days=1)
#
#             day_orders = Order.objects.filter(created_at__gte=day_start, created_at__lt=day_end)
#
#             daily_stats.append(
#                 {
#                     "date": day.strftime("%Y-%m-%d"),
#                     "orders": day_orders.count(),
#                     "revenue": float(
#                         day_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0
#                     ),
#                 }
#             )
#
#         # Статистика по статусам
#         status_stats = []
#         for status_code, status_name in Order.STATUS_CHOICES:
#             count = Order.objects.filter(created_at__gte=start_date, status=status_code).count()
#             status_stats.append({"status": status_name, "count": count})
#
#         # Формирование отчета
#         report_data = {
#             "period": {
#                 "start_date": start_date.strftime("%Y-%m-%d"),
#                 "end_date": end_date.strftime("%Y-%m-%d"),
#                 "days": days,
#             },
#             "summary": {
#                 "total_orders": total_orders,
#                 "total_revenue": float(total_revenue),
#                 "avg_order_value": float(avg_order_value),
#                 "total_customers": User.objects.filter(role="customer").count(),
#                 "total_products": Product.objects.count(),
#             },
#             "top_products": list(top_products),
#             "category_stats": category_stats,
#             "daily_stats": daily_stats,
#             "status_stats": status_stats,
#         }
#
#         if format_type == "json":
#             self.stdout.write(json.dumps(report_data, indent=2, ensure_ascii=False))
#         else:
#             self.print_text_report(report_data)
#
#     def print_text_report(self, data):
#         self.stdout.write(self.style.SUCCESS("📊 АНАЛИТИЧЕСКИЙ ОТЧЕТ"))
#         self.stdout.write("=" * 50)
#
#         # Период
#         period = data["period"]
#         self.stdout.write(
#             f"📅 Период: {period['start_date']} - {period['end_date']} ({period['days']} дней)"
#         )
#
#         # Основная статистика
#         summary = data["summary"]
#         self.stdout.write("\n📈 ОСНОВНАЯ СТАТИСТИКА:")
#         self.stdout.write(f"   🛒 Заказов: {summary['total_orders']}")
#         self.stdout.write(f"   💰 Выручка: {summary['total_revenue']:,.0f} ₽")
#         self.stdout.write(f"   📊 Средний чек: {summary['avg_order_value']:,.0f} ₽")
#         self.stdout.write(f"   👥 Покупателей: {summary['total_customers']}")
#         self.stdout.write(f"   📦 Товаров: {summary['total_products']}")
#
#         # Топ товары
#         self.stdout.write("\n🏆 ТОП-5 ТОВАРОВ:")
#         for i, product in enumerate(data["top_products"][:5], 1):
#             self.stdout.write(f"   {i}. {product['product__name']} - {product['total_sold']} шт.")
#
#         # Категории
#         self.stdout.write("\n🏷️ ПРОДАЖИ ПО КАТЕГОРИЯМ:")
#         sorted_categories = sorted(data["category_stats"], key=lambda x: x["revenue"], reverse=True)
#         for category in sorted_categories[:5]:
#             self.stdout.write(f"   • {category['name']}: {category['revenue']:,.0f} ₽")
#
#         # Статусы заказов
#         self.stdout.write("\n📋 СТАТУСЫ ЗАКАЗОВ:")
#         for status in data["status_stats"]:
#             if status["count"] > 0:
#                 self.stdout.write(f"   • {status['status']}: {status['count']}")
#
#         self.stdout.write("\n" + "=" * 50)
#         self.stdout.write(self.style.SUCCESS("✅ Отчет сформирован успешно!"))
