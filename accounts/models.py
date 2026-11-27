
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        MANAGEMENT_ADMIN = 'MANAGEMENT_ADMIN', 'Management Admin'
        DONOR = 'DONOR', 'Waste Donor'
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        LABOUR = 'LABOUR', 'Labour'

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.DONOR
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
