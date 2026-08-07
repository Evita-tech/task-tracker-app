from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

]