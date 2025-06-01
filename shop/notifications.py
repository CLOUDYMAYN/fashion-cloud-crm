import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User

logger = logging.getLogger(__name__)


class NotificationService:
    """Сервис для отправки уведомлений"""

    @staticmethod
    def send_order_confirmation(order):
        """Отправка подтверждения заказа покупателю"""
        try:
            subject = f"Подтверждение заказа #{order.id} - FashionStore"

            html_message = render_to_string(
                "shop/emails/order_confirmation.html",
                {
                    "order": order,
                    "customer_name": f"{order.first_name} {order.last_name}",
                },
            )

            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                html_message=html_message,
                fail_silently=False,
            )

            logger.info(f"Order confirmation sent for order #{order.id}")
            return True

        except Exception as e:
            logger.error(
                f"Failed to send order confirmation for order #{order.id}: {str(e)}"
            )
            return False

    @staticmethod
    def send_low_stock_alert(product):
        """Отправка уведомления о низком остатке товара"""
        try:
            # Получаем всех администраторов
            admins = User.objects.filter(role__in=["boss", "manager"])

            if not admins.exists():
                return False

            subject = f"⚠️ Низкий остаток товара: {product.name}"

            html_message = render_to_string(
                "shop/emails/low_stock_alert.html", {"product": product}
            )

            plain_message = strip_tags(html_message)

            admin_emails = [admin.email for admin in admins if admin.email]

            if admin_emails:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=admin_emails,
                    html_message=html_message,
                    fail_silently=False,
                )

                logger.info(f"Low stock alert sent for product: {product.name}")
                return True

        except Exception as e:
            logger.error(
                f"Failed to send low stock alert for product {product.name}: {str(e)}"
            )
            return False

    @staticmethod
    def send_new_order_alert(order):
        """Отправка уведомления о новом заказе администраторам"""
        try:
            admins = User.objects.filter(role__in=["boss", "manager"])

            if not admins.exists():
                return False

            subject = f"🛒 Новый заказ #{order.id} - FashionStore"

            html_message = render_to_string(
                "shop/emails/new_order_alert.html", {"order": order}
            )

            plain_message = strip_tags(html_message)

            admin_emails = [admin.email for admin in admins if admin.email]

            if admin_emails:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=admin_emails,
                    html_message=html_message,
                    fail_silently=False,
                )

                logger.info(f"New order alert sent for order #{order.id}")
                return True

        except Exception as e:
            logger.error(
                f"Failed to send new order alert for order #{order.id}: {str(e)}"
            )
            return False
