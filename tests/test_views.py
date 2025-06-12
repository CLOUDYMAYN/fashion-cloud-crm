from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Category, Product

User = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")  # nosec
        self.user = User.objects.create_user(username="testuser", password="testpass123")  # nosec
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpass123", role="manager"
        )  # nosec
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            description="Test description",
            price=100.00,
            stock=10,
        )

    def test_home_view(self):
        response = self.client.get(reverse("shop:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FashionStore")

    def test_product_list_view(self):
        response = self.client.get(reverse("shop:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_product_detail_view(self):
        response = self.client.get(reverse("shop:product_detail", args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_dashboard_requires_admin(self):
        response = self.client.get(reverse("shop:dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_with_admin_user(self):
        self.client.login(username="admin", password="adminpass123")  # nosec
        self.client.login(username="admin", password="adminpass123")  # nosec
        response = self.client.get(reverse("shop:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_requires_login(self):
        response = self.client.post(reverse("shop:add_to_cart", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
