import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Order, Product
from .notifications import NotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    """Обработчик создания нового заказа"""
    if created:
        # Отправляем подтверждение покупателю
        NotificationService.send_order_confirmation(instance)

        # Уведомляем администраторов
        NotificationService.send_new_order_alert(instance)

        logger.info(f"Order #{instance.id} created and notifications sent")


@receiver(pre_save, sender=Product)
def product_stock_check(sender, instance, **kwargs):
    """Проверка остатков товара при изменении"""
    if instance.pk:  # Если товар уже существует
        try:
            old_instance = Product.objects.get(pk=instance.pk)

            # Если остаток стал меньше 5 и раньше был больше
            if instance.stock < 5 and old_instance.stock >= 5:
                # Отправляем уведомление о низком остатке
                NotificationService.send_low_stock_alert(instance)
                logger.info(f"Low stock alert sent for product: {instance.name}")

        except Product.DoesNotExist:
            pass
