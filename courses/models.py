from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость курса',
        default=0.00
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен для покупки'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class CourseAccess(models.Model):
    """Модель доступа к курсу."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_accesses'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='accesses'
    )
    access_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Доступ к курсу'
        verbose_name_plural = 'Доступы к курсам'
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} -> {self.course}"


class Lesson(models.Model):
    """Модель урока."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
        null=True,
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    name = models.CharField(max_length=100, unique=True, verbose_name='Название группы', null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('id',)

    def __str__(self):
        return self.name
