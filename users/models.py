from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models




class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    courses = models.ManyToManyField(
        'courses.Course',
        related_name='students',
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


User = get_user_model()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь',
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Баланс',
        default=1000.00
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        """Переопределяем метод save для проверки отрицательного баланса."""
        if self.amount < 0:
            raise ValueError("Баланс не может быть отрицательным")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.amount}"


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions',
                             verbose_name='Пользователь', null=True)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='subscriptions',
                               verbose_name='Курс', null=True)
    group = models.ForeignKey('courses.Group', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Группа', null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} -> {self.course} ({self.group})"

