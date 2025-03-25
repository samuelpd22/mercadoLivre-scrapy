from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_produto, name='buscar_produto'),

]