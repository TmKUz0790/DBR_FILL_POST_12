# sales/urls.py

from django.urls import path
from .views import sales_entry, sales_entry_pdf_view, sales_success

urlpatterns = [
    path('', sales_entry, name='sales-entry'),
    path('success/', sales_success, name='sales-success'),
    path('pdf/', sales_entry_pdf_view, name='sales-pdf'),
]
