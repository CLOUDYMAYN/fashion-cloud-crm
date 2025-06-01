from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Order, OrderItem, Product, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "is_staff"]
    list_filter = ["role", "is_staff", "is_superuser"]
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("role", "phone", "address")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "available", "created_at"]
    list_filter = ["available", "category", "created_at"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_price", "created_at"]
    list_filter = ["status", "created_at"]
    inlines = [OrderItemInline]
