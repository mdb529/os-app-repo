from django.contrib import admin
from .models import Drug,Manufacturer,NDC

admin.site.register(Drug)
admin.site.register(Manufacturer)
admin.site.register(NDC)