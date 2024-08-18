from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем доступ админам и для чтения
        if request.user.is_staff or request.method in SAFE_METHODS:
            return True
        
        # Проверяем, есть ли у пользователя подписка на курс
        course_id = view.kwargs.get('course_id')
        return Subscription.objects.filter(user=request.user, course_id=course_id).exists()

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ админам и для чтения
        if request.user.is_staff or request.method in SAFE_METHODS:
            return True
        
        # Проверяем, есть ли у пользователя подписка на курс, к которому относится урок
        return Subscription.objects.filter(user=request.user, course=obj.course).exists()



class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
