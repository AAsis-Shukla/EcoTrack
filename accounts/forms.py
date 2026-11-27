
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from managements.models import Management, Zone
from donors.models import Donor


class ManagementRegistrationForm(UserCreationForm):

    organization_name = forms.CharField(max_length=200)
    registration_number = forms.CharField(max_length=100)

    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)

    description = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class DonorRegistrationForm(UserCreationForm):

    donor_type = forms.ChoiceField(
        choices=Donor.DonorType.choices
    )

    name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(required=False)

    management = forms.ModelChoiceField(
        queryset=Management.objects.filter(is_active=True)
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.filter(is_active=True)
    )

    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()

        management = cleaned_data.get('management')
        zone = cleaned_data.get('zone')

        if management and zone:
            if zone.management_id != management.id:
                raise forms.ValidationError(
                    "Selected zone does not belong to this management."
                )

        return cleaned_data
