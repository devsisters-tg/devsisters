from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('merci/', views.success, name='success'),
]
