from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    ROLE_CHOICES = [
        ("customer", "Покупатель"),
        ("manager", "Менеджер"),
        ("boss", "Руководитель"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Добавляем related_name для избежания конфликтов
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="shop_users",
        related_query_name="shop_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="shop_users",
        related_query_name="shop_user",
    )

    def is_admin_user(self):
        return self.role in ["boss", "manager"]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает обработки"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("cancelled", "Отменен"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    city = models.CharField(max_length=100, verbose_name="Город")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price * self.quantity
