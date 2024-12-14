from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.sales_entry, name='sales_entry'),
]
