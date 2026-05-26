from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from .models import LabSession
import datetime


class LabSessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass1234!')
        now = timezone.now()
        self.session = LabSession.objects.create(
            title='Test Session',
            requested_by=self.user,
            start_time=now,
            end_time=now + datetime.timedelta(hours=2),
        )

    def test_str(self):
        self.assertIn('Test Session', str(self.session))

    def test_duration(self):
        self.assertEqual(self.session.duration_hours(), 2.0)

    def test_default_status_is_pending(self):
        self.assertEqual(self.session.status, LabSession.STATUS_PENDING)


class SessionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.researcher = User.objects.create_user(username='res', password='pass1234!', role='researcher')
        self.tech = User.objects.create_user(username='tech', password='pass1234!', role='technician')
        now = timezone.now()
        self.session = LabSession.objects.create(
            title='Session A',
            requested_by=self.researcher,
            start_time=now + datetime.timedelta(days=1),
            end_time=now + datetime.timedelta(days=1, hours=3),
        )

    def test_list_requires_login(self):
        r = self.client.get(reverse('schedules:session_list'))
        self.assertEqual(r.status_code, 302)

    def test_researcher_sees_own_sessions(self):
        self.client.login(username='res', password='pass1234!')
        r = self.client.get(reverse('schedules:session_list'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Session A')

    def test_approve_blocked_for_researcher(self):
        self.client.login(username='res', password='pass1234!')
        r = self.client.get(reverse('schedules:session_approve', args=[self.session.pk]))
        self.assertRedirects(r, reverse('schedules:session_list'))

    def test_approve_allowed_for_tech(self):
        self.client.login(username='tech', password='pass1234!')
        r = self.client.get(reverse('schedules:session_approve', args=[self.session.pk]))
        self.assertEqual(r.status_code, 200)
