from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import Equipment, Category, MaintenanceLog
import datetime


class EquipmentModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Robots')
        self.eq = Equipment.objects.create(name='Arm Robot', serial_number='SN-001', category=self.cat)

    def test_str(self):
        self.assertIn('Arm Robot', str(self.eq))

    def test_is_available(self):
        self.assertTrue(self.eq.is_available())
        self.eq.status = Equipment.STATUS_IN_USE
        self.assertFalse(self.eq.is_available())


class EquipmentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass1234!', role='admin')
        self.researcher = User.objects.create_user(username='res', password='pass1234!', role='researcher')
        self.cat = Category.objects.create(name='Sensors')
        self.eq = Equipment.objects.create(name='LiDAR', serial_number='SN-002', category=self.cat)

    def test_list_requires_login(self):
        r = self.client.get(reverse('inventory:equipment_list'))
        self.assertEqual(r.status_code, 302)

    def test_list_accessible_when_logged_in(self):
        self.client.login(username='res', password='pass1234!')
        r = self.client.get(reverse('inventory:equipment_list'))
        self.assertEqual(r.status_code, 200)

    def test_create_blocked_for_researcher(self):
        self.client.login(username='res', password='pass1234!')
        r = self.client.get(reverse('inventory:equipment_create'))
        self.assertRedirects(r, reverse('inventory:equipment_list'))

    def test_create_allowed_for_admin(self):
        self.client.login(username='admin', password='pass1234!')
        r = self.client.get(reverse('inventory:equipment_create'))
        self.assertEqual(r.status_code, 200)

    def test_delete_blocked_for_researcher(self):
        self.client.login(username='res', password='pass1234!')
        r = self.client.post(reverse('inventory:equipment_delete', args=[self.eq.pk]))
        self.assertRedirects(r, reverse('inventory:equipment_list'))
        self.assertTrue(Equipment.objects.filter(pk=self.eq.pk).exists())
