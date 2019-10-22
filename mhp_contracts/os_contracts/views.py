from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Drug,Manufacturer,NDC

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

def single_manufacturer(request,manufacturer_name):
    try:
        single_manufacturer = Manufacturer.objects.get(name=manufacturer_name)
    except Manufacturer.DoesNotExist:
        raise Http404('Manufacturer does not exist.')

    context = {
        "single_manufacturer": single_manufacturer,
        "manufacturer_drugs": single_manufacturer.drugs.all()
    }
    return render(request, 'os_contracts/single_manufacturer.html',context)
