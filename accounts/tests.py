from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin1', password='pass1234!', role='admin')
        self.tech = User.objects.create_user(username='tech1', password='pass1234!', role='technician')
        self.researcher = User.objects.create_user(username='res1', password='pass1234!', role='researcher')

    def test_role_methods(self):
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_technician())
        self.assertTrue(self.tech.is_technician())
        self.assertTrue(self.researcher.is_researcher())

    def test_str(self):
        self.assertIn('admin1', str(self.admin))


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234!', role='researcher')

    def test_login_page_loads(self):
        r = self.client.get(reverse('accounts:login'))
        self.assertEqual(r.status_code, 200)

    def test_register_page_loads(self):
        r = self.client.get(reverse('accounts:register'))
        self.assertEqual(r.status_code, 200)

    def test_login_valid(self):
        r = self.client.post(reverse('accounts:login'), {'username': 'testuser', 'password': 'pass1234!'})
        self.assertRedirects(r, '/')

    def test_login_invalid(self):
        r = self.client.post(reverse('accounts:login'), {'username': 'testuser', 'password': 'wrong'})
        self.assertEqual(r.status_code, 200)

    def test_profile_requires_login(self):
        r = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(r, '/accounts/login/?next=/accounts/profile/')

    def test_user_list_admin_only(self):
        self.client.login(username='testuser', password='pass1234!')
        r = self.client.get(reverse('accounts:user_list'))
        self.assertRedirects(r, '/')
