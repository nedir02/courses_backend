from django.contrib import admin
from .models import Course, Lesson, CourseAccess, Group


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка для курсов."""
    list_display = ('title', 'start_date', 'author', 'price', 'is_available')
    search_fields = ('title', 'author')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка для уроков."""
    list_display = ('title', 'link', 'course')
    search_fields = ('title', 'link')


@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    """Админка для уроков."""
    list_display = ('user', 'course', 'access_date')


@admin.register(Group)
class LessonAdmin(admin.ModelAdmin):
    """Админка для уроков."""
    list_display = ('name',)
