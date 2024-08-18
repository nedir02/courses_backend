from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, CourseAccess, Group
from rest_framework.templatetags.rest_framework import data
from users.models import Subscription

from users.models import Balance




class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    def get_queryset(self):
        """Фильтрует доступные для покупки курсы."""
        return self.queryset.filter(is_available=True)

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        course = get_object_or_404(Course, pk=pk)
        user = request.user

        try:
            balance = user.balance
        except Balance.DoesNotExist:
            return Response(
                {"error": "Баланс пользователя не найден."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not course.is_available:
            return Response(
                {"error": "Курс недоступен для покупки."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.courses.filter(pk=course.pk).exists():
            return Response(
                {"error": "Вы уже приобрели этот курс."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if balance.amount < course.price:
            return Response(
                {"error": "Недостаточно бонусов для покупки."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Списываем бонусы
            balance.amount -= course.price
            balance.save()

            # Подписка на курс
            user.courses.add(course)

            # Предоставление доступа к курсу
            CourseAccess.objects.create(user=user, course=course)

            # Найти группы для этого курса через подписки
            groups = Group.objects.filter(subscriptions__course=course).distinct()

            # Проверить, существует ли группа с менее чем 10 студентами
            group = None
            for g in groups:
                if g.subscriptions.count() < 30:
                    group = g
                    break

            # Если подходящей группы нет, создать новую
            if group is None:
                group = Group.objects.create(name=f'Группа для {course.title}')
                group.name = f'Группа для {course.title} (ID: {group.pk})'
                group.save()

            # Создать подписку для пользователя в найденной или новой группе
            Subscription.objects.create(user=user, course=course, group=group)

        return Response(
            {"message": "Курс успешно приобретен и доступ предоставлен."},
            status=status.HTTP_200_OK
        )



class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления подписками."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Если вернуть подписки только текущего пользователя:
        return self.queryset.filter(user=self.request.user)