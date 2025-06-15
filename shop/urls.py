from django.contrib.auth import views as auth_views
from django.urls import path

from . import api_views, views

app_name = "shop"

urlpatterns = [
    # Customer URLs
    path("", views.home, name="home"),
    path("catalog/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contacts/", views.contacts, name="contacts"),
    # Auth URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="shop/login.html"),
        name="login",
    ),
    path("logout/", views.custom_logout, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    # Cart URLs
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    # Admin URLs
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/advanced/", views.advanced_dashboard, name="advanced_dashboard"),
    path("api/dashboard/", views.dashboard_api, name="dashboard_api"),
    # API URLs
    path(
        "api/dashboard-stats/",
        api_views.dashboard_stats_api,
        name="dashboard_stats_api",
    ),
    path("api/export-data/", api_views.export_data_api, name="export_data_api"),
    path(
        "api/bulk-update-products/",
        api_views.bulk_update_products_api,
        name="bulk_update_products_api",
    ),
    path(
        "api/notifications/",
        api_views.real_time_notifications_api,
        name="notifications_api",
    ),
    # Product management
    path("dashboard/products/", views.admin_products, name="admin_products"),
    path(
        "dashboard/products/create/",
        views.admin_product_create,
        name="admin_product_create",
    ),
    path(
        "dashboard/products/<int:product_id>/edit/",
        views.admin_product_edit,
        name="admin_product_edit",
    ),
    path(
        "dashboard/products/<int:product_id>/delete/",
        views.admin_product_delete,
        name="admin_product_delete",
    ),
    # Category management
    path("dashboard/categories/", views.admin_categories, name="admin_categories"),
    path(
        "dashboard/categories/create/",
        views.admin_category_create,
        name="admin_category_create",
    ),
    # Order management
    path("dashboard/orders/", views.admin_orders, name="admin_orders"),
    path(
        "dashboard/orders/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
    # User management (boss only)
    path("dashboard/users/", views.admin_users, name="admin_users"),
    path(
        "dashboard/users/<int:user_id>/role/",
        views.admin_user_role,
        name="admin_user_role",
    ),
    # Utility URLs
    path("login-redirect/", views.login_redirect_view, name="login_redirect"),
    path("health/", views.health_check, name="health_check"),
    path("login-redirect/", views.login_redirect_view, name="login_redirect"),
    path("create-superuser/", views.create_superuser_temp),
]
