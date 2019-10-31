from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="index"),
    path("drugs/",views.drugs,name="drugs"),
    path("manufacturers/", views.manufacturers, name="manufacturers"),
    path("manufacturers/<slug:slug>", views.single_manufacturer, name="single_manufacturer"),
    path("transactions/", views.transactions,name="transactions")
]