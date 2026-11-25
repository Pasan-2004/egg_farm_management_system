
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import FeedStock, FeedConsumption
from .forms import FeedStockForm, FeedConsumptionForm


@login_required
def feed_list(request):
    stocks = FeedStock.objects.all()

    consumptions = FeedConsumption.objects.select_related(
        'batch', 'feed'
    ).order_by('-date', '-id')

    return render(
        request,
        'feed/feed_list.html',
        {
            'stocks': stocks,
            'consumptions': consumptions
        }
    )


@login_required
def add_feed(request):
    if request.method == 'POST':
        form = FeedStockForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('feed_list')
    else:
        form = FeedStockForm()

    return render(
        request,
        'feed/feed_form.html',
        {
            'form': form,
            'title': 'Add Feed Stock'
        }
    )


@login_required
def add_consumption(request):
    if request.method == 'POST':
        form = FeedConsumptionForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('feed_list')

            except ValidationError as error:
                form.add_error(None, error)
    else:
        form = FeedConsumptionForm()

    return render(
        request,
        'feed/feed_form.html',
        {
            'form': form,
            'title': 'Add Feed Consumption'
        }
    )
