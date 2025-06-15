import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.shortcuts import redirect
from .decorators import admin_required, boss_required
from .forms import (
    CategoryForm,
    CheckoutForm,
    CustomUserCreationForm,
    ProductForm,
    UserRoleForm,
)
from .models import Cart, CartItem, Category, Order, OrderItem, Product, User
from django.contrib.auth.models import User


def get_base_template(user):
    """Определяет базовый шаблон в зависимости от роли пользователя"""
    if user.role == "boss":
        return "shop/base_boss.html"
    elif user.role == "manager":
        return "shop/base_manager.html"
    else:
        return "shop/base_dashboard.html"


def home(request):
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    return render(
        request,
        "shop/home.html",
        {"featured_products": featured_products, "categories": categories},
    )


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(
        request,
        "shop/product_list.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": category_slug,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "shop/product_detail.html", {"product": product})


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("shop:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "shop/signup.html", {"form": form})


def custom_logout(request):
    logout(request)
    return JsonResponse({"success": True})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({"success": True, "cart_items_count": cart.get_total_items()})


@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []

    return render(request, "shop/cart.html", {"cart_items": cart_items})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("shop:cart")


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.error(request, "Ваша корзина пуста")
            return redirect("shop:cart")
    except Cart.DoesNotExist:
        messages.error(request, "Ваша корзина пуста")
        return redirect("shop:cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )

            cart.items.all().delete()
            messages.success(request, f"Заказ #{order.id} успешно оформлен!")
            return redirect("shop:home")
    else:
        form = CheckoutForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            }
        )

    return render(request, "shop/checkout.html", {"form": form, "cart": cart})


@admin_required
def dashboard(request):
    # Основная статистика
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum("total_price"))["total_price__sum"] or 0
    total_products = Product.objects.count()
    total_customers = User.objects.filter(role="customer").count()

    # Статистика за последние 30 дней
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
    recent_revenue = recent_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0
    recent_orders_count = recent_orders.count()

    # Продажи по дням (последние 7 дней)
    sales_by_day = []
    for i in range(7):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        day_orders = Order.objects.filter(created_at__gte=day_start, created_at__lt=day_end)

        sales_by_day.append(
            {
                "date": day.strftime("%d.%m"),
                "orders": day_orders.count(),
                "revenue": float(day_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0),
            }
        )

    sales_by_day.reverse()

    # Последние заказы
    recent_orders_list = Order.objects.select_related("user").order_by("-created_at")[:10]

    # Статистика по категориям (реальные данные)
    category_stats = []
    total_sold_items = OrderItem.objects.aggregate(total=Sum("quantity"))["total"] or 1

    for category in Category.objects.all():
        sold_items = (
            OrderItem.objects.filter(product__category=category).aggregate(total=Sum("quantity"))[
                "total"
            ]
            or 0
        )

        percentage = round((sold_items / total_sold_items) * 100, 1) if total_sold_items > 0 else 0

        category_stats.append(
            {"name": category.name, "percentage": percentage, "sold_items": sold_items}
        )

    # Сортируем по проценту продаж
    category_stats.sort(key=lambda x: x["percentage"], reverse=True)

    # Топ товары по продажам
    top_products = (
        OrderItem.objects.values("product__name", "product__price")
        .annotate(
            total_sold=Sum("quantity"),
            total_revenue=Sum("quantity") * Sum("price") / Sum("quantity"),
        )
        .order_by("-total_sold")[:5]
    )

    # Товары с низким остатком (меньше 5 штук)
    low_stock_products = Product.objects.filter(stock__lt=5, available=True).order_by("stock")[:5]

    # Статистика по статусам заказов
    order_status_stats = []
    for status_code, status_name in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status_code).count()
        order_status_stats.append({"status": status_name, "count": count, "code": status_code})

    # Средний чек
    avg_order_value = Order.objects.aggregate(avg=Avg("total_price"))["avg"] or 0

    # Рост по сравнению с предыдущим месяцем
    prev_month_start = thirty_days_ago - timedelta(days=30)
    prev_month_orders = Order.objects.filter(
        created_at__gte=prev_month_start, created_at__lt=thirty_days_ago
    )
    prev_month_revenue = prev_month_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0
    prev_month_count = prev_month_orders.count()

    # Вычисляем процент роста
    revenue_growth = 0
    orders_growth = 0

    if prev_month_revenue > 0:
        revenue_growth = round(
            ((recent_revenue - prev_month_revenue) / prev_month_revenue) * 100, 1
        )

    if prev_month_count > 0:
        orders_growth = round(
            ((recent_orders_count - prev_month_count) / prev_month_count) * 100, 1
        )

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_products": total_products,
        "total_customers": total_customers,
        "recent_orders_count": recent_orders_count,
        "recent_revenue": recent_revenue,
        "sales_by_day": json.dumps(sales_by_day),  # Конвертируем в JSON для JavaScript
        "recent_orders": recent_orders_list,
        "category_stats": category_stats,
        "top_products": top_products,
        "low_stock_products": low_stock_products,
        "order_status_stats": order_status_stats,
        "avg_order_value": avg_order_value,
        "revenue_growth": revenue_growth,
        "orders_growth": orders_growth,
        "base_template": get_base_template(request.user),
    }

    return render(request, "shop/dashboard.html", context)


@admin_required
def advanced_dashboard(request):
    """Продвинутая аналитика"""
    return render(
        request,
        "shop/advanced_dashboard.html",
        {
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def dashboard_api(request):
    """API endpoint для получения данных dashboard в JSON формате"""
    # Продажи по дням (последние 30 дней)
    sales_data = []
    for i in range(30):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        day_orders = Order.objects.filter(created_at__gte=day_start, created_at__lt=day_end)

        sales_data.append(
            {
                "date": day.strftime("%Y-%m-%d"),
                "orders": day_orders.count(),
                "revenue": float(day_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0),
            }
        )

    sales_data.reverse()

    # Статистика по категориям
    category_data = []
    total_sold_items = OrderItem.objects.aggregate(total=Sum("quantity"))["total"] or 1

    for category in Category.objects.all():
        sold_items = (
            OrderItem.objects.filter(product__category=category).aggregate(total=Sum("quantity"))[
                "total"
            ]
            or 0
        )

        percentage = round((sold_items / total_sold_items) * 100, 1) if total_sold_items > 0 else 0

        category_data.append(
            {"name": category.name, "percentage": percentage, "sold_items": sold_items}
        )

    return JsonResponse({"sales_data": sales_data, "category_data": category_data, "success": True})


@admin_required
def admin_products(request):
    products = Product.objects.select_related("category").order_by("-created_at")
    return render(
        request,
        "shop/admin_products.html",
        {
            "products": products,
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар успешно создан!")
            return redirect("shop:admin_products")
    else:
        form = ProductForm()
    return render(
        request,
        "shop/admin_product_form.html",
        {
            "form": form,
            "title": "Создать товар",
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар успешно обновлен!")
            return redirect("shop:admin_products")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "shop/admin_product_form.html",
        {
            "form": form,
            "title": "Редактировать товар",
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Товар успешно удален!")
        return redirect("shop:admin_products")
    return render(
        request,
        "shop/admin_product_delete.html",
        {
            "product": product,
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_categories(request):
    categories = Category.objects.all()
    return render(
        request,
        "shop/admin_categories.html",
        {
            "categories": categories,
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория успешно создана!")
            return redirect("shop:admin_categories")
    else:
        form = CategoryForm()
    return render(
        request,
        "shop/admin_category_form.html",
        {
            "form": form,
            "title": "Создать категорию",
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_orders(request):
    orders = Order.objects.select_related("user").order_by("-created_at")
    return render(
        request,
        "shop/admin_orders.html",
        {
            "orders": orders,
            "base_template": get_base_template(request.user),
        },
    )


@admin_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "shop/admin_order_detail.html",
        {
            "order": order,
            "base_template": get_base_template(request.user),
        },
    )


@boss_required
def admin_users(request):
    users = User.objects.all().order_by("-date_joined")
    return render(
        request,
        "shop/admin_users.html",
        {
            "users": users,
            "base_template": get_base_template(request.user),
        },
    )


@login_required
def login_redirect_view(request):
    user = request.user
    if user.is_superuser or user.is_staff:
        return redirect('shop:dashboard')  # на admin-панель
    else:
        return redirect('shop:home')  # обычный пользователь


@boss_required
def admin_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Роль пользователя {user.username} успешно изменена!")
            return redirect("shop:admin_users")
    else:
        form = UserRoleForm(instance=user)
    return render(
        request,
        "shop/admin_user_role.html",
        {
            "form": form,
            "user": user,
            "base_template": get_base_template(request.user),
        },
    )


def contacts(request):
    return render(request, "shop/contacts.html")


    """Перенаправление после входа в зависимости от роли"""
@login_required
def login_redirect_view(request):
    if request.user.is_admin_user():
        return redirect("shop:dashboard")
    else:
        return redirect("shop:home")


def health_check(request):
    """Health check endpoint для мониторинга"""
    try:
        # Проверяем подключение к базе данных
        User.objects.count()

        return JsonResponse(
            {
                "status": "healthy",
                "timestamp": timezone.now().isoformat(),
                "version": "1.0.0",
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": timezone.now().isoformat(),
            },
            status=503,
        )
