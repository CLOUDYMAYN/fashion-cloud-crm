import json
from datetime import timedelta

from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .decorators import admin_required
from .models import Category, Order, OrderItem, Product, User


@admin_required
@require_http_methods(["GET"])
def dashboard_stats_api(request):
    """API для получения статистики dashboard"""

    # Период для анализа
    days = int(request.GET.get("days", 30))
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    # Основная статистика
    stats = {
        "total_orders": Order.objects.filter(created_at__gte=start_date).count(),
        "total_revenue": float(
            Order.objects.filter(created_at__gte=start_date).aggregate(total=Sum("total_price"))[
                "total"
            ]
            or 0
        ),
        "avg_order_value": float(
            Order.objects.filter(created_at__gte=start_date).aggregate(avg=Avg("total_price"))[
                "avg"
            ]
            or 0
        ),
        "total_customers": User.objects.filter(role="customer").count(),
        "active_products": Product.objects.filter(available=True).count(),
    }

    # Продажи по дням
    daily_sales = []
    for i in range(days):
        day = start_date + timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        day_orders = Order.objects.filter(created_at__gte=day_start, created_at__lt=day_end)

        daily_sales.append(
            {
                "date": day.strftime("%Y-%m-%d"),
                "orders": day_orders.count(),
                "revenue": float(day_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0),
            }
        )

    # Топ товары
    top_products = list(
        OrderItem.objects.filter(order__created_at__gte=start_date)
        .values("product__name", "product__price")
        .annotate(
            total_sold=Sum("quantity"),
            total_revenue=Sum("quantity") * Sum("price") / Sum("quantity"),
        )
        .order_by("-total_sold")[:10]
    )

    # Статистика по категориям
    category_stats = []
    for category in Category.objects.all():
        sold_items = (
            OrderItem.objects.filter(
                order__created_at__gte=start_date, product__category=category
            ).aggregate(total=Sum("quantity"))["total"]
            or 0
        )

        revenue = (
            OrderItem.objects.filter(
                order__created_at__gte=start_date, product__category=category
            ).aggregate(total=Sum("quantity") * Sum("price") / Sum("quantity"))["total"]
            or 0
        )

        category_stats.append(
            {"name": category.name, "sold_items": sold_items, "revenue": float(revenue)}
        )

    return JsonResponse(
        {
            "success": True,
            "stats": stats,
            "daily_sales": daily_sales,
            "top_products": top_products,
            "category_stats": category_stats,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days,
            },
        }
    )


@admin_required
@require_http_methods(["GET"])
def export_data_api(request):
    """API для экспорта данных"""

    data_type = request.GET.get("type", "orders")
    request.GET.get("format", "json")

    if data_type == "orders":
        orders = Order.objects.select_related("user").prefetch_related("items__product")
        data = []

        for order in orders:
            order_data = {
                "id": order.id,
                "customer": f"{order.first_name} {order.last_name}",
                "email": order.email,
                "phone": order.phone,
                "total_price": float(order.total_price),
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "product": item.product.name,
                        "quantity": item.quantity,
                        "price": float(item.price),
                    }
                    for item in order.items.all()
                ],
            }
            data.append(order_data)

    elif data_type == "products":
        products = Product.objects.select_related("category")
        data = [
            {
                "id": product.id,
                "name": product.name,
                "category": product.category.name,
                "price": float(product.price),
                "stock": product.stock,
                "available": product.available,
                "created_at": product.created_at.isoformat(),
            }
            for product in products
        ]

    elif data_type == "customers":
        customers = User.objects.filter(role="customer")
        data = [
            {
                "id": customer.id,
                "username": customer.username,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "date_joined": customer.date_joined.isoformat(),
                "orders_count": Order.objects.filter(user=customer).count(),
            }
            for customer in customers
        ]

    else:
        return JsonResponse({"error": "Invalid data type"}, status=400)

    return JsonResponse(
        {
            "success": True,
            "data": data,
            "count": len(data),
            "exported_at": timezone.now().isoformat(),
        }
    )


@admin_required
@require_http_methods(["POST"])
def bulk_update_products_api(request):
    """API для массового обновления товаров"""

    try:
        data = json.loads(request.body)
        action = data.get("action")
        product_ids = data.get("product_ids", [])

        if not product_ids:
            return JsonResponse({"error": "No products selected"}, status=400)

        products = Product.objects.filter(id__in=product_ids)

        if action == "activate":
            products.update(available=True)
            message = f"Активировано {products.count()} товаров"

        elif action == "deactivate":
            products.update(available=False)
            message = f"Деактивировано {products.count()} товаров"

        elif action == "update_stock":
            stock_value = data.get("stock_value", 0)
            products.update(stock=stock_value)
            message = f"Обновлен остаток для {products.count()} товаров"

        elif action == "update_price":
            price_multiplier = data.get("price_multiplier", 1.0)
            for product in products:
                product.price = product.price * price_multiplier
                product.save()
            message = f"Обновлены цены для {products.count()} товаров"

        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

        return JsonResponse(
            {"success": True, "message": message, "updated_count": products.count()}
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@admin_required
@require_http_methods(["GET"])
def real_time_notifications_api(request):
    """API для получения уведомлений в реальном времени"""

    # Последние заказы (за последний час)
    recent_orders = Order.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=1)
    ).count()

    # Товары с низким остатком
    low_stock_count = Product.objects.filter(stock__lt=5, available=True).count()

    # Новые пользователи (за последний день)
    new_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=1), role="customer"
    ).count()

    # Заказы требующие обработки
    pending_orders = Order.objects.filter(status="pending").count()

    notifications = []

    if recent_orders > 0:
        notifications.append(
            {
                "type": "info",
                "title": "Новые заказы",
                "message": f"Получено {recent_orders} новых заказов за последний час",
                "count": recent_orders,
            }
        )

    if low_stock_count > 0:
        notifications.append(
            {
                "type": "warning",
                "title": "Низкий остаток",
                "message": f"{low_stock_count} товаров требуют пополнения",
                "count": low_stock_count,
            }
        )

    if new_users > 0:
        notifications.append(
            {
                "type": "success",
                "title": "Новые пользователи",
                "message": f"{new_users} новых пользователей зарегистрировались",
                "count": new_users,
            }
        )

    if pending_orders > 0:
        notifications.append(
            {
                "type": "urgent",
                "title": "Ожидают обработки",
                "message": f"{pending_orders} заказов ожидают обработки",
                "count": pending_orders,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "notifications": notifications,
            "timestamp": timezone.now().isoformat(),
        }
    )
