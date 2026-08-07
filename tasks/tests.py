from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Project, Task


class TaskTrackerTests(TestCase):

    def setUp(self):
        # Create Manager and Team Member groups
        self.manager_group = Group.objects.create(name='Manager')
        self.team_member_group = Group.objects.create(name='Team Member')

        # Create a Manager user
        self.manager = User.objects.create_user(username='manager1', password='testpass123')
        self.manager.groups.add(self.manager_group)

        # Create a Team Member user
        self.team_member = User.objects.create_user(username='member1', password='testpass123')
        self.team_member.groups.add(self.team_member_group)

        # Create a sample
        self.project = Project.objects.create(name='Sample Project', description='A test project')

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)


    def test_manager_can_create_project(self):
         self.client.login(username='manager1', password='testpass123')
         response = self.client.post('/projects/create/', {
            'name': 'New Project',
            'description': 'Created by manager'
        })
         self.assertTrue(Project.objects.filter(name='New Project').exists())

    def test_team_member_cannot_create_project(self):
         self.client.login(username='member1', password='testpass123')
         response = self.client.post('/projects/create/', {
            'name': 'Blocked Project',
            'description': 'Should not be created'
        })
         self.assertFalse(Project.objects.filter(name='Blocked Project').exists())       
    def test_manager_can_create_task(self):
        self.client.login(username='manager1', password='testpass123')
        response = self.client.post('/tasks/create/', {
            'project': self.project.id,
            'title': 'New Task',
            'description': 'Created by manager',
            'status': 'todo',
            'assigned_to': self.team_member.id,
        })
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_team_member_cannot_create_task(self):
        self.client.login(username='member1', password='testpass123')
        response = self.client.post('/tasks/create/', {
            'project': self.project.id,
            'title': 'Blocked Task',
            'description': 'Should not be created',
            'status': 'todo',
        })
        self.assertFalse(Task.objects.filter(title='Blocked Task').exists())

    def test_registration_creates_user(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
