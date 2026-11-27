
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.views.decorators.http import require_POST

from .models import Management, Zone
from .forms import ZoneForm


def get_user_management(user):
    return get_object_or_404(
        Management,
        admin=user
    )


@login_required
def zone_list(request):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    zones = Zone.objects.filter(
        management=management
    ).order_by('name')

    return render(request, 'zone_list.html', {
        'zones': zones,
        'management': management,
    })


@login_required
def zone_create(request):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    if request.method == 'POST':
        form = ZoneForm(request.POST)

        if form.is_valid():
            zone = form.save(commit=False)
            zone.management = management
            zone.save()

            messages.success(request, 'Zone added successfully.')
            return redirect('managements:zone_list')
    else:
        form = ZoneForm()

    return render(request, 'zone_form.html', {
        'form': form,
        'page_title': 'Add New Zone',
    })


@login_required
def zone_update(request, pk):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    zone = get_object_or_404(
        Zone,
        pk=pk,
        management=management
    )

    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)

        if form.is_valid():
            form.save()
            messages.success(request, 'Zone updated successfully.')
            return redirect('managements:zone_list')
    else:
        form = ZoneForm(instance=zone)

    return render(request, 'zone_form.html', {
        'form': form,
        'page_title': 'Edit Zone',
    })


@login_required
@require_POST
def zone_toggle_status(request, pk):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    zone = get_object_or_404(
        Zone,
        pk=pk,
        management=management
    )

    zone.is_active = not zone.is_active
    zone.save(update_fields=['is_active'])

    messages.success(request, 'Zone status updated.')
    return redirect('managements:zone_list')


@login_required
@require_POST
def zone_delete(request, pk):
    if request.user.role != 'MANAGEMENT_ADMIN':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    management = get_user_management(request.user)

    zone = get_object_or_404(
        Zone,
        pk=pk,
        management=management
    )

    try:
        zone.delete()
        messages.success(request, 'Zone deleted successfully.')
    except ProtectedError:
        messages.error(
            request,
            'This zone cannot be deleted because donors are assigned to it. '
            'You can deactivate it instead.'
        )

    return redirect('managements:zone_list')
