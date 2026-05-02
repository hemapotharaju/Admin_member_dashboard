from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('api/signup/', views.SignupView.as_view(), name='api_signup'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutView.as_view(), name='api_logout'),
    path('api/projects/', views.ProjectListCreateView.as_view(), name='api_projects'),
    path('api/tasks/', views.TaskListCreateView.as_view(), name='api_tasks'),
    path('api/tasks/<int:pk>/', views.TaskDetailUpdateView.as_view(), name='api_task_detail'),
    path('api/dashboard-summary/', views.DashboardSummaryView.as_view(), name='api_dashboard_summary'),
]
