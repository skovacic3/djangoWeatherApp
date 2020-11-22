
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('city', views.specific_city, name="citydetails"),
    path('delete', views.delete_city, name="delete_city")
]