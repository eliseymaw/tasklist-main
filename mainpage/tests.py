import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task, Geoposition, Profile
from .forms import TaskForm, RegisterForm, LoginForm, ProfileForm, GeopositionForm


# Тесты для моделей
class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.geop = Geoposition.objects.create(lat=55.75, lon=37.61)

    def test_geoposition_str(self):
        self.assertEqual(str(self.geop), "Lat: 55.75, Lon: 37.61")

    def test_profile_creation_and_str(self):
        profile = Profile.objects.create(user=self.user, bio='bio text', location='Москва')
        self.assertEqual(str(profile), 'testuser')
        self.assertEqual(profile.bio, 'bio text')

    def test_task_creation_and_str(self):
        task = Task.objects.create(
            owner=self.user,
            title='Test Task',
            description='Test Description',
            geop=self.geop,
            date_start=timezone.now(),
            deadline=timezone.now() + timedelta(days=1),
            repeat_type='d',
            repeat_i=1
        )
        self.assertEqual(str(task), 'Test Task')
        self.assertEqual(task.description, 'Test Description')
    
    def test_is_overdue(self):
        task = Task.objects.create(
            owner=self.user,
            title='Test Task',
            description='Test Description',
            geop=self.geop,
            date_start=timezone.now() - timedelta(days=2),
            deadline=timezone.now() - timedelta(days=1),
            repeat_type='d',
            repeat_i=1
        )
        self.assertTrue(task.is_overdue())

    def test_next_repeat(self):
        task = Task.objects.create(
            owner=self.user,
            title='Test Task',
            description='Test Description',
            geop=self.geop,
            date_start=timezone.now() - timedelta(days=2),
            deadline=timezone.now() - timedelta(days=1),
            repeat_type='d',
            repeat_i=1
        )
        self.assertEqual(task.next_repeat(), task.deadline + timedelta(days=1))


# Тесты для форм
class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_register_form_valid(self):
        form_data = {'username': 'newuser', 'password1': 'newpass123', 'password2': 'newpass123'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = {'username': '', 'password1': 'newpass123', 'password2': 'newpass123'}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_valid(self):
        geop = Geoposition.objects.create(lat=55.75, lon=37.61)
        form_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'date_start': timezone.now(),
            'deadline': timezone.now() + timedelta(days=1),
            'repeat_type': 'd',
            'repeat_i': 1,
            'geop': geop.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        form_data = {'title': '', 'description': 'Test Description'}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())


# Тесты для представлений (views)
class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_create_task_view_post(self):
        geop = Geoposition.objects.create(lat=55.75, lon=37.61)
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'date_start': timezone.now(),
            'deadline': timezone.now() + timedelta(days=1),
            'repeat_type': 'd',
            'repeat_i': 1,
            'geop': geop.id
        }
        response = self.client.post(reverse('create_task'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation

    def test_task_list_view(self):
        Task.objects.create(
            owner=self.user,
            title='Test Task',
            description='Test Description',
            geop=None,
            date_start=timezone.now(),
            deadline=timezone.now() + timedelta(days=1),
            repeat_type='d',
            repeat_i=1
        )
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_list_json_view(self):
        task = Task.objects.create(
            owner=self.user,
            title='Test Task',
            description='Test Description',
            geop=None,
            date_start=timezone.now(),
            deadline=timezone.now() + timedelta(days=1),
            repeat_type='d',
            repeat_i=1
        )
        response = self.client.get(reverse('task_list_json'))
        self.assertEqual(response.status_code, 200)
        tasks_json = json.loads(response.content)
        self.assertEqual(len(tasks_json['tasks']), 1)
        self.assertEqual(tasks_json['tasks'][0]['title'], 'Test Task')


# Тесты для модели профиля
class ProfileTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, bio='bio text', location='Москва')
        self.assertEqual(profile.bio, 'bio text')
        self.assertEqual(profile.location, 'Москва')

    def test_edit_profile_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')