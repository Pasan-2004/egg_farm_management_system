from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import HealthRecord
from .forms import HealthRecordForm
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages


@login_required
def health_list(request):

    today = timezone.localdate()
    upcoming_date = today + timedelta(days=7)

    records = HealthRecord.objects.select_related(
        'batch'
    ).order_by('-date', '-id')

    search = request.GET.get('search', '').strip()
    selected_type = request.GET.get('type', '').strip()

    if search:
        from django.db.models import Q

        records = records.filter(
            Q(description__icontains=search) |
            Q(medicine_or_vaccine__icontains=search)
        )

    if selected_type:
        records = records.filter(
            record_type=selected_type
        )

    upcoming_records = HealthRecord.objects.filter(
        next_due_date__gte=today,
        next_due_date__lte=upcoming_date
    ).select_related('batch').order_by('next_due_date')

    context = {
        'records': records,
        'upcoming_records': upcoming_records,
        'search': search,
        'selected_type': selected_type,
        'record_types': HealthRecord._meta.get_field(
            'record_type'
        ).choices,
        'today': today,
        'upcoming_date': upcoming_date,
    }

    return render(
        request,
        'health/health_list.html',
        context
    )


@login_required
def add_health(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Health record added successfully!")
            return redirect('health_list')
    else:
        form = HealthRecordForm()

    return render(
        request,
        'health/health_form.html',
        {
            'form': form,
            'title': 'Add Health Record'
        }
    )


@login_required
def edit_health(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Health record updated successfully!"
            )
            return redirect('health_list')

    else:
        form = HealthRecordForm(instance=record)

    return render(
        request,
        'health/health_form.html',
        {
            'form': form,
            'title': 'Edit Health Record'
        }
    )


@login_required
def delete_health(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Health record deleted successfully!")
        return redirect('health_list')

    return render(
        request,
        'health/health_confirm_delete.html',
        {'record': record}
    )
