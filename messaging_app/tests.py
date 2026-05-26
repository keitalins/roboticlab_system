from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from .models import Message, Notification


class MessageModelTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass1234!')
        self.recipient = User.objects.create_user(username='recipient', password='pass1234!')
        self.msg = Message.objects.create(sender=self.sender, recipient=self.recipient, subject='Hello', body='World')

    def test_str(self):
        self.assertIn('Hello', str(self.msg))

    def test_default_unread(self):
        self.assertFalse(self.msg.is_read)


class MessagingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.u1 = User.objects.create_user(username='u1', password='pass1234!')
        self.u2 = User.objects.create_user(username='u2', password='pass1234!')
        self.msg = Message.objects.create(sender=self.u1, recipient=self.u2, subject='Hi', body='There')

    def test_inbox_requires_login(self):
        r = self.client.get(reverse('messaging_app:inbox'))
        self.assertEqual(r.status_code, 302)

    def test_inbox_shows_received_messages(self):
        self.client.login(username='u2', password='pass1234!')
        r = self.client.get(reverse('messaging_app:inbox'))
        self.assertContains(r, 'Hi')

    def test_reading_message_marks_as_read(self):
        self.client.login(username='u2', password='pass1234!')
        self.client.get(reverse('messaging_app:message_detail', args=[self.msg.pk]))
        self.msg.refresh_from_db()
        self.assertTrue(self.msg.is_read)

    def test_compose_sends_message(self):
        self.client.login(username='u1', password='pass1234!')
        r = self.client.post(reverse('messaging_app:compose'), {
            'recipient': self.u2.pk,
            'subject': 'Test Subject',
            'body': 'Test Body',
        })
        self.assertRedirects(r, reverse('messaging_app:inbox'))
        self.assertTrue(Message.objects.filter(subject='Test Subject').exists())
