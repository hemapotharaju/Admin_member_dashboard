from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Task, Profile
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'dashboard/login.html')


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'dashboard/signup.html')


@login_required(login_url='login')
def dashboard_page(request):
    return render(request, 'dashboard/dashboard.html')


class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', Profile.ROLE_MEMBER)

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, role=role)
        return Response({'detail': 'Account created successfully.'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        Profile.objects.get_or_create(user=user)
        return Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        project.members.add(self.request.user)


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(project__owner=user) | Q(project__members=user) | Q(assignee=user)).distinct()

    def perform_create(self, serializer):
        task = serializer.save()
        if task.assignee and task.assignee not in task.project.members.all():
            task.project.members.add(task.assignee)


class TaskDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(project__owner=user) | Q(project__members=user) | Q(assignee=user)).distinct()


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(Q(project__owner=user) | Q(project__members=user) | Q(assignee=user)).distinct()
        projects = Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()

        return Response({
            'project_count': projects.count(),
            'task_count': tasks.count(),
            'status_summary': tasks.values('status').annotate(count=Count('status')), 
            'overdue_count': tasks.filter(status=Task.STATUS_OVERDUE).count(),
        })
