from urllib import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes



# 🔐 REGISTER USER
@api_view(['POST'])

def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"})
    return Response(serializer.errors)


# 📌 GET ALL TASKS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# ➕ ADD TASK
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_task(request):
    print(request.data)
    print(request.FILES)

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    print(serializer.errors)
    return Response(serializer.errors, status=400)


# ❌ DELETE TASK
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response({"message": "Deleted"})


# ✅ TOGGLE COMPLETE
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.completed = not task.completed
    task.save()
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    total_tasks = Task.objects.filter(user=user).count()
    completed_tasks = Task.objects.filter(
        user=user,
        completed=True
    ).count()

    pending_tasks = Task.objects.filter(
        user=user,
        completed=False
    ).count()

    return Response({
        "username": user.username,
        "email": user.email,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    })