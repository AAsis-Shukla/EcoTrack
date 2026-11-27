
from django.db import models
from django.conf import settings


class Management(models.Model):

    name = models.CharField(max_length=200, unique=True)

    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_organization'
    )

    registration_number = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField()
    phone = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Zone(models.Model):

    management = models.ForeignKey(
        Management,
        on_delete=models.CASCADE,
        related_name='zones'
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('management', 'name')

    def __str__(self):
        return f"{self.name} - {self.management.name}"
