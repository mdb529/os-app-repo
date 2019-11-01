from django.db.models import Avg, Sum, Min, Max, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Drug, Manufacturer, NDC, Contract, Purchase
import pandas as pd
import math
from datetime import date, datetime, timedelta
import bisect
from workdays import workday,networkdays
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import os

def get_qtr_dates():
    current_date = date.today()
    qtr_start_dates = [date(current_date.year, month, 1) for month in (1, 4, 7, 10)]
    idx = bisect.bisect(qtr_start_dates, current_date)
    if idx == 1:
        qtr_begin, qtr_end = (date(2019,1,1),date(2019,3,31))
    elif idx == 2:
        qtr_begin, qtr_end = (date(2019,4,1),date(2019,6,30))
    elif idx == 3:
        qtr_begin, qtr_end = (date(2019,7,1),date(2019,9,30))
    else:
        qtr_begin, qtr_end = (date(2019,10,1),date(2019,12,31))
    return (qtr_begin, qtr_end)

    # us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    # working_days_in_qtr = len(pd.date_range(start=qtr_begin, end=qtr_end, freq=us_bd))
    # working_days_passed = len(pd.date_range(start=qtr_begin, end=current_date, freq=us_bd))
    # working_days_remaining = len(pd.date_range(start=current_date, end=qtr_end, freq=us_bd)) - 1
    # curr_qtr_date_range = pd.date_range(start=qtr_begin,end=qtr_end)



def index(request):
    context = {
        "drugs": Drug.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request,'purchasing/index.html', context)

def drugs(request):
    context = {
        'drugs': Drug.objects.all()
    }

    return render(request, 'purchasing/drugs.html',context)

def manufacturers(request):
    context = {
        "manufacturers": Manufacturer.objects.all(),
    }
    return render(request, 'purchasing/manufacturers.html',context)

def single_manufacturer(request,slug):
    try:
        single_manufacturer = Manufacturer.objects.get(slug=slug)
    except Manufacturer.DoesNotExist:
        raise Http404('Manufacturer does not exist.')

    context = {
        "single_manufacturer": single_manufacturer,
        "manufacturer_drugs": single_manufacturer.drugs.all()
    }
    return render(request, 'purchasing/single_manufacturer.html',context)

def purchases(request):
    all_purchases = Purchase.objects.all()
    at_total_dqty = all_purchases.aggregate(Sum('delivered_qty'))
    qtd_purchases = all_purchases.filter(invoice_date__range=[qtr_begin, qtr_end])
    purchases = Purchase.objects.filter(invoice_date__range=[qtr_begin,qtr_end])
    qty = purchases.aggregate(Sum('delivered_qty'))
    eqty = purchases.aggregate(Sum('extended_delivered_qty'))
    qt_total_dqty = qtd_purchases.aggregate(Sum('delivered_qty'))
    drug_list = all_purchases.order_by().values('drug_name').distinct()
    
    context = {
        'drugs': Drug.objects.all(),
        'all_purchases': all_purchases,
        'at_total_dqty':at_total_dqty,
        'qtd_purchases': qtd_purchases,
        'purchases':purchases,
        'qty':qty,
        'eqty':eqty,
        'drug_list': drug_list
    }
    return render(request, 'purchasing/purchases.html',context)