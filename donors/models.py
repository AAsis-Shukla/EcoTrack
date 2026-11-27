
from django.db import models
from django.conf import settings
from managements.models import Management, Zone


def clean(self):
    from django.core.exceptions import ValidationError

    if self.management_id and self.zone_id:
        if self.zone.management_id != self.management_id:
            raise ValidationError({
                'zone': 'Selected zone does not belong to this management.'
            })

class Donor(models.Model):

    class DonorType(models.TextChoices):
        HOUSEHOLD = 'HOUSEHOLD', 'Household'
        SOCIETY = 'SOCIETY', 'Residential Society'
        SHOP = 'SHOP', 'Shop'
        PUBLIC_PLACE = 'PUBLIC_PLACE', 'Public Place'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donor_profile'
    )

    management = models.ForeignKey(
        Management,
        on_delete=models.PROTECT,
        related_name='donors'
    )

    zone = models.ForeignKey(
        Zone,
        on_delete=models.PROTECT,
        related_name='donors'
    )

    donor_type = models.CharField(
        max_length=20,
        choices=DonorType.choices
    )

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_donor_type_display()})"
