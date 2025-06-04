import os

from django.contrib.auth import get_user_model
from django.test import TestCase

from shop.models import Cart, CartItem, Category, Product

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(..., password=os.getenv("TEST_PASSWORD", "defaultpass"))  # nosec
        User.objects.create_user(..., password=os.getenv("TEST_PASSWORD", "defaultpass"))  # nosec

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.role, "customer")

    def test_is_admin_user(self):
        self.assertFalse(self.user.is_admin_user())

        self.user.role = "manager"
        self.assertTrue(self.user.is_admin_user())


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            description="Test description",
            price=100.00,
            stock=10,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.00)
        self.assertTrue(self.product.available)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            ..., password=os.getenv("TEST_PASSWORD", "defaultpass")
        )  # nosec
        self.user = User.objects.create_user(
            ..., password=os.getenv("TEST_PASSWORD", "defaultpass")
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
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_total_price(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(self.cart.get_total_price(), 200.00)

    def test_cart_total_items(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        self.assertEqual(self.cart.get_total_items(), 3)
