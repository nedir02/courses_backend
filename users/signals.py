from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Balance

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    """Создаем баланс пользователя при создании пользователя."""
    if created:
        Balance.objects.create(user=instance)
