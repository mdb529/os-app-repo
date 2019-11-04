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

def index(request):
    context = {
        "drugs": Drug.objects.all(),
        "manufacturers": Manufacturer.objects.all()
    }
    return render(request,'purchasing/index.html', context)

def drugs(request):
    context = {
        'drugs': Drug.objects.all(),
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


def single_drug(request,slug):
    try:
        single_drug = Drug.objects.get(slug=slug)
    except Drug.DoesNotExist:
        raise Http404('Drug does not exist.')
    
    q1_contract_qty = single_drug.contract_qty(1)
    q2_contract_qty = single_drug.contract_qty(2)
    q3_contract_qty = single_drug.contract_qty(3)
    q4_contract_qty = single_drug.contract_qty(4)

    q1_purchases = single_drug.q1.aggregate(Sum('total'))['total__sum']
    q2_purchases = single_drug.q2.aggregate(Sum('total'))['total__sum']
    q3_purchases = single_drug.q3.aggregate(Sum('total'))['total__sum']
    q4_purchases = single_drug.q4.aggregate(Sum('total'))['total__sum']

    contract = single_drug.contract
    contract_rebate_schedule = contract.rebate_schedule
    growth_tiers = contract_rebate_schedule['growth_tiers']
    volume_tiers = contract_rebate_schedule['volume_tiers']

    ndc_list = NDC.objects.filter(drug_name=single_drug.name)

    context = {
        "single_drug": single_drug,
        "ndc_list": ndc_list,
        "q1_contract_qty": q1_contract_qty,
        "q2_contract_qty": q2_contract_qty,
        "q3_contract_qty": q3_contract_qty,
        "q4_contract_qty": q4_contract_qty,
        "q1_purchases": q1_purchases,
        "q2_purchases": q2_purchases,
        "q3_purchases": q3_purchases,
        "q4_purchases": q4_purchases,
        "contract": contract,
        "contract_rebate_schedule": contract_rebate_schedule,
        "growth_tiers": growth_tiers,
        "volume_tiers":volume_tiers
    }
    return render(request, 'purchasing/single_drug.html',context)


def purchases(request):
    all_purchases = Purchase.objects.all()
    drug_list = all_purchases.order_by().values('drug_name').distinct()
    
    context = {
        'drugs': Drug.objects.all(),
        'all_purchases': all_purchases,
        'drug_list': drug_list
    }
    return render(request, 'purchasing/purchases.html', context)

def test_style(request):
    drug = Drug.objects.get(name='Abraxane')
    ndc = NDC.objects.get(drug_name='Abraxane')

    contract = drug.contract
    contract_rebate_schedule = contract.rebate_schedule
    growth_tiers = contract_rebate_schedule['growth_tiers']
    volume_tiers = contract_rebate_schedule['volume_tiers']
    context = {
        "drug": drug,
        "ndc": ndc,
        "contract": contract,
        "contract_rebate_schedule": contract_rebate_schedule,
        "growth_tiers": growth_tiers,
        "volume_tiers":volume_tiers
    }
    return render(request, 'purchasing/test_style.html',context)