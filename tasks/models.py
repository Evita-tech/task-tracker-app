from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Project(models.Model):
    name =models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  


class Task(models.Model):
    STATUS_CHOICES =[
        ('todo','To Do'),
        ('in_progress','In progress'),
        ('done','Done'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True,blank=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"