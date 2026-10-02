from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('projects/create/', views.create_project, name='create_project'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/update/', views.update_task_status, name='update_task_status'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'), 
    path('hello/',views.hello_world,name='hello'),
]