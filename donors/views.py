
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from managements.models import Management
from .models import Donor


def get_user_management(user):
    return get_object_or_404(Management, admin=user)


def management_admin_required(request):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return False
    return True


@login_required
def donor_list(request):
    if not management_admin_required(request):
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    donors = Donor.objects.filter(
        management=management
    ).select_related('user', 'zone').order_by('-created_at')

    # Filter by approval status
    status = request.GET.get('status', '')
    valid_statuses = [choice[0] for choice in Donor.Status.choices]

    if status in valid_statuses:
        donors = donors.filter(status=status)

    # Filter by donor type
    donor_type = request.GET.get('type', '')
    valid_types = [choice[0] for choice in Donor.DonorType.choices]

    if donor_type in valid_types:
        donors = donors.filter(donor_type=donor_type)

    context = {
        'donors': donors,
        'selected_status': status,
        'selected_type': donor_type,
        'status_choices': Donor.Status.choices,
        'type_choices': Donor.DonorType.choices,
    }

    return render(request, 'donor_list.html', context)


@login_required
def donor_detail(request, pk):
    if not management_admin_required(request):
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    donor = get_object_or_404(
        Donor.objects.select_related('user', 'zone', 'management'),
        pk=pk,
        management=management
    )

    return render(request, 'donor_detail.html', {
        'donor': donor,
    })


@login_required
@require_POST
def donor_approve(request, pk):
    if not management_admin_required(request):
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    donor = get_object_or_404(
        Donor,
        pk=pk,
        management=management
    )

    if donor.status != Donor.Status.PENDING:
        messages.warning(request, 'This donor is not awaiting approval.')
        return redirect('donors:donor_detail', pk=donor.pk)

    donor.status = Donor.Status.APPROVED
    donor.is_active = True
    donor.save(update_fields=['status', 'is_active', 'updated_at'])

    messages.success(request, 'Donor approved successfully.')
    return redirect('donors:donor_detail', pk=donor.pk)


@login_required
@require_POST
def donor_reject(request, pk):
    if not management_admin_required(request):
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    donor = get_object_or_404(
        Donor,
        pk=pk,
        management=management
    )

    if donor.status != Donor.Status.PENDING:
        messages.warning(request, 'Only pending registrations can be rejected.')
        return redirect('donors:donor_detail', pk=donor.pk)

    donor.status = Donor.Status.REJECTED
    donor.save(update_fields=['status', 'updated_at'])

    messages.success(request, 'Donor registration rejected.')
    return redirect('donors:donor_detail', pk=donor.pk)


@login_required
@require_POST
def donor_toggle_status(request, pk):
    if not management_admin_required(request):
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    donor = get_object_or_404(
        Donor,
        pk=pk,
        management=management
    )

    if donor.status != Donor.Status.APPROVED:
        messages.warning(
            request,
            'Only approved donors can be activated or deactivated.'
        )
        return redirect('donors:donor_detail', pk=donor.pk)

    donor.is_active = not donor.is_active
    donor.save(update_fields=['is_active', 'updated_at'])

    messages.success(request, 'Donor account status updated.')
    return redirect('donors:donor_detail', pk=donor.pk)
