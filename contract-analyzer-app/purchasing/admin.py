from django.contrib import admin
from .models import Drug,Manufacturer,NDC,Contract,Purchase

admin.site.register(Drug)
admin.site.register(Manufacturer)
admin.site.register(NDC)
admin.site.register(Contract)
admin.site.register(Purchase)