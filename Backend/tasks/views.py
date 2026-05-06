from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


@api_view(["GET", "POST"])
def task_list_create(request):
    if request.method == "GET":
        group_id = request.GET.get("group_id")

        if group_id:
            tasks = Task.objects.filter(group_id=group_id).order_by("-created_at")
        else:
            tasks = Task.objects.all().order_by("-created_at")

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["PUT", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found"}, status=404)

    if request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    task.delete()
    return Response({"detail": "Task deleted"})