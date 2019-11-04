from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="index"),
    path("drugs/",views.drugs,name="drugs"),
    path("drugs/<slug:slug>",views.single_drug,name="single_drug"),
    path("manufacturers/", views.manufacturers, name="manufacturers"),
    path("manufacturers/<slug:slug>", views.single_manufacturer, name="single_manufacturer"),
    path("test",views.test_style,name="test_style"),
    # path("purchases/", views.transactions,name="purchases")
]