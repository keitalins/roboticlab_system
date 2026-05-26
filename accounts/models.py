from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_TECHNICIAN = 'technician'
    ROLE_RESEARCHER = 'researcher'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_TECHNICIAN, 'Lab Technician'),
        (ROLE_RESEARCHER, 'Student / Researcher'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_RESEARCHER)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def is_technician(self):
        return self.role == self.ROLE_TECHNICIAN

    def is_researcher(self):
        return self.role == self.ROLE_RESEARCHER

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
