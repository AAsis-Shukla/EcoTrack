
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from managements.models import Management
from donors.models import Donor


@login_required
def home(request):

    user = request.user

    if user.role == 'MANAGEMENT_ADMIN':
        return redirect('dashboard:management_dashboard')

    elif user.role == 'DONOR':
        return redirect('dashboard:donor_dashboard')

    messages.error(request, 'You do not have dashboard access.')
    return redirect('accounts:home')


@login_required
def management_dashboard(request):

    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    try:
        management = Management.objects.get(admin=request.user)
    except Management.DoesNotExist:
        messages.error(request, 'Management profile not found.')
        return redirect('accounts:home')

    donors = Donor.objects.filter(management=management)

    context = {
    'management': management,

    'total_donors': donors.count(),

    'pending_donors': donors.filter(
        status='PENDING'
    ).count(),

    'approved_donors': donors.filter(
        status='APPROVED'
    ).count(),

    'total_zones': management.zones.count(),

    'latest_donors': donors.order_by('-created_at')[:5],

    'zones': management.zones.all(),
}

    return render(
        request,
        'management_dashboard.html',
        context
    )



@login_required
def donor_dashboard(request):
    if request.user.role != 'DONOR':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    try:
        donor = request.user.donor_profile
    except Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found.')
        return redirect('accounts:home')

    if donor.status != Donor.Status.APPROVED:
        messages.warning(
            request,
            'Your registration is awaiting approval or has been rejected.'
        )
        return redirect('accounts:home')

    if not donor.is_active:
        messages.warning(
            request,
            'Your donor account is currently inactive.'
        )
        return redirect('accounts:home')

    return render(request, 'donor_dashboard.html', {
        'donor': donor,
    })


# from django.shortcuts import redirect, render
# from django.contrib.auth.decorators import login_required


# @login_required
# def home(request):

#     user = request.user

#     if user.role == 'MANAGEMENT_ADMIN':
#         return redirect('dashboard:management_dashboard')

#     elif user.role == 'DONOR':
#         return redirect('dashboard:donor_dashboard')

#     else:
#         return redirect('accounts:home')


# @login_required
# def management_dashboard(request):

#     if request.user.role != 'MANAGEMENT_ADMIN':
#         return redirect('dashboard:home')

#     return render(
#         request,
#         'management_dashboard.html'
#     )


# @login_required
# def donor_dashboard(request):

#     if request.user.role != 'DONOR':
#         return redirect('dashboard:home')

#     return render(
#         request,
#         'donor_dashboard.html'
#     )