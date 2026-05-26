from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import LabReport


class LabReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass1234!')
        self.report = LabReport.objects.create(title='Test Report', author=self.user, content='Some content')

    def test_str(self):
        self.assertEqual(str(self.report), 'Test Report')

    def test_default_status_draft(self):
        self.assertEqual(self.report.status, LabReport.STATUS_DRAFT)


class ReportViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='pass1234!', role='researcher')
        self.tech = User.objects.create_user(username='tech', password='pass1234!', role='technician')
        self.report = LabReport.objects.create(title='My Report', author=self.author, content='Content here')

    def test_list_requires_login(self):
        r = self.client.get(reverse('lab_reports:report_list'))
        self.assertEqual(r.status_code, 302)

    def test_author_can_see_own_report(self):
        self.client.login(username='author', password='pass1234!')
        r = self.client.get(reverse('lab_reports:report_list'))
        self.assertContains(r, 'My Report')

    def test_submit_changes_status(self):
        self.client.login(username='author', password='pass1234!')
        self.client.post(reverse('lab_reports:report_submit', args=[self.report.pk]))
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, LabReport.STATUS_SUBMITTED)

    def test_review_blocked_for_researcher(self):
        self.client.login(username='author', password='pass1234!')
        r = self.client.get(reverse('lab_reports:report_review', args=[self.report.pk]))
        self.assertRedirects(r, reverse('lab_reports:report_list'))
