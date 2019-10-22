from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="index"),
    path("drugs/",views.drugs,name="drugs"),
    path("manufacturers/", views.manufacturers, name="manufacturers"),
    path("manufacturers/<slug:manufacturer_name>", views.single_manufacturer, name="single_manufacturer")
]