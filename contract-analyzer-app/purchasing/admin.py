from django.contrib import admin
from .models import Drug,Manufacturer,NDC,Purchase

admin.site.register(Drug)
admin.site.register(Manufacturer)
admin.site.register(NDC)
admin.site.register(Purchase)