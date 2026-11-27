
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.urls import reverse_lazy

from .forms import (
    ManagementRegistrationForm,
    DonorRegistrationForm
)

from .models import User
from managements.models import Management
from donors.models import Donor


def home(request):
    return render(request, 'home.html')


@transaction.atomic
def management_register(request):

    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = ManagementRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = User.Role.MANAGEMENT_ADMIN
            user.email = form.cleaned_data['email']
            user.save()

            Management.objects.create(
                admin=user,
                name=form.cleaned_data['organization_name'],
                registration_number=form.cleaned_data['registration_number'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode'],
                description=form.cleaned_data['description']
            )

            login(request, user)

            messages.success(
                request,
                'Management account created successfully!'
            )

            return redirect('dashboard:home')

    else:
        form = ManagementRegistrationForm()

    return render(
        request,
        'management_register.html',
        {'form': form}
    )


@transaction.atomic
def donor_register(request):

    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = User.Role.DONOR
            user.email = form.cleaned_data['email']
            user.save()

            Donor.objects.create(
                user=user,
                management=form.cleaned_data['management'],
                zone=form.cleaned_data['zone'],
                donor_type=form.cleaned_data['donor_type'],
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode']
            )

            login(request, user)

            messages.success(
                request,
                'Donor registration submitted successfully!'
            )

            return redirect('dashboard:home')

    else:
        form = DonorRegistrationForm()

    return render(
        request,
        'donor_register.html',
        {'form': form}
    )


class EcoTrackLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:home')


@login_required
def user_logout(request):

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')

    return redirect('accounts:home')
