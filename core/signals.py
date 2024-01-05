from django.dispatch import receiver
from django.db.models.signals import post_save

from core.models import OrderingFood


# @receiver(post_save, sender=OrderingFood)
# def order_item_post_save(sender, instance: OrderingFood, created, *args, **kwargs):
#     if created:
#         food = instance.food
#         instance.price = product.price
#         instance.save()