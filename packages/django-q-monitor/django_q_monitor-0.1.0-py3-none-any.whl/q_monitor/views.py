from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_q.models import Task, Schedule
from django_q.tasks import async_task
from .serializers import TaskSerializer, ScheduleSerializer

# Se vuoi tenerlo aperto per test usa AllowAny, altrimenti IsAdminUser
PERMISSION_CLASS = IsAdminUser 

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all().order_by('-started')
    serializer_class = TaskSerializer
    permission_classes = [PERMISSION_CLASS]

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """
        Endpoint: POST /api/monitor/tasks/{id}/retry/
        Retries an existing task with the same arguments.
        """
        task = self.get_object()
        new_id = async_task(task.func, *task.args, **task.kwargs)
        return Response({
            'status': 'retried', 
            'original_task': task.id, 
            'new_task_id': new_id
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def cleanup(self, request):
        """
        Endpoint: DELETE /api/monitor/tasks/cleanup/
        Deletes all completed or failed tasks to free up space.
        """
        count, _ = Task.objects.exclude(func__isnull=True).delete()
        return Response({'status': 'cleaned', 'deleted_count': count})

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all().order_by('next_run')
    serializer_class = ScheduleSerializer
    permission_classes = [PERMISSION_CLASS]

class FailureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.filter(success=False).order_by('-started')
    serializer_class = TaskSerializer
    permission_classes = [PERMISSION_CLASS]