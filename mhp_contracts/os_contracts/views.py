from django.db.models import Avg, Sum, Min, Max, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Drug, Manufacturer, NDC, Contract
from data_loader.models import Transaction
import pandas as pd
import math
from datetime import date, datetime, timedelta
import bisect
from workdays import workday,networkdays
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
import os

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
us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
working_days_in_qtr = len(pd.date_range(start=qtr_begin, end=qtr_end, freq=us_bd))
working_days_passed = len(pd.date_range(start=qtr_begin, end=current_date, freq=us_bd))
working_days_remaining = len(pd.date_range(start=current_date, end=qtr_end, freq=us_bd)) - 1
curr_qtr_date_range = pd.date_range(start=qtr_begin,end=qtr_end)

# Create your views here.
def index(request):
    context = {
        "drugs": Drug.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request,'os_contracts/index.html', context)

def drugs(request):
    context = {
        'drugs': Drug.objects.all()
    }

    return render(request, 'os_contracts/drugs.html',context)

def manufacturers(request):
    context = {
        "manufacturers": Manufacturer.objects.all(),
    }
    return render(request, 'os_contracts/manufacturers.html',context)

def single_manufacturer(request,slug):
    try:
        single_manufacturer = Manufacturer.objects.get(slug=slug)
    except Manufacturer.DoesNotExist:
        raise Http404('Manufacturer does not exist.')

    context = {
        "single_manufacturer": single_manufacturer,
        "manufacturer_drugs": single_manufacturer.drugs.all()
    }
    return render(request, 'os_contracts/single_manufacturer.html',context)

def transactions(request):
    all_transactions = Transaction.objects.all()
    at_total_dqty = all_transactions.aggregate(Sum('delivered_quantity'))
    qtd_transactions = all_transactions.filter(invoice_date__range=[qtr_begin, qtr_end])
    qt_total_dqty = qtd_transactions.aggregate(Sum('delivered_quantity'))
    drug_list = all_transactions.order_by().values('drug_name').distinct()
    
    context = {
        'drugs': Drug.objects.all(),
        'all_transactions': all_transactions,
        'at_total_dqty':at_total_dqty,
        'qtd_transactions': qtd_transactions,
        'qt_total_dqty':qt_total_dqty,
        'drug_list': drug_list
    }
    return render(request, 'os_contracts/transactions.html',context)