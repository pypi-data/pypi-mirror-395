from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')
router.register(r'schedules', views.ScheduleViewSet, basename='schedules')
router.register(r'failures', views.FailureViewSet, basename='failures')

urlpatterns = [
    path('', include(router.urls)),
]