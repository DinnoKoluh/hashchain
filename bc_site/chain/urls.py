from django.urls import path

from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('blockchain', views.blockchain, name='blockchain'),
]