
import json
from decimal import Decimal
from django.forms import formset_factory

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal objects to float
        return super().default(obj)


# Configure logging
from django.shortcuts import render
from .forms import SalesEntryForm
from .google_sheets import append_to_sheet, get_dispatcher_names, get_client_names,get_car_numbers
from datetime import date, datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


def get_sales_form_class(dispatcher_choices, client_choices, car_choices):
    class CustomSalesEntryForm(SalesEntryForm):
        def __init__(self, *args, **kwargs):
            # Inject the choices here
            kwargs['dispatcher_choices'] = dispatcher_choices
            kwargs['client_choices'] = client_choices
            kwargs['car_choices'] = car_choices
            super().__init__(*args, **kwargs)
    return CustomSalesEntryForm


import json
from decimal import Decimal
from django.forms import formset_factory
from django.shortcuts import render
from .forms import SalesEntryForm
from .google_sheets import append_to_sheet, append_to_nachislenie_sheet, get_dispatcher_names, get_client_names, get_car_numbers
from datetime import date
import logging

logger = logging.getLogger(__name__)

# def get_sales_form_class(dispatcher_choices, client_choices, car_choices):
#     class CustomSalesEntryForm(SalesEntryForm):
#         def __init__(self, *args, **kwargs):
#             kwargs['dispatcher_choices'] = dispatcher_choices
#             kwargs['client_choices'] = client_choices
#             kwargs['car_choices'] = car_choices
#             super().__init__(*args, **kwargs)
#     return CustomSalesEntryForm
#
# def sales_entry(request):
#     dispatcher_names = get_dispatcher_names()
#     dispatcher_choices = [(name.strip(), name.strip()) for name in dispatcher_names if name.strip()]
#     client_names = get_client_names()
#     client_choices = [(name.strip(), name.strip()) for name in client_names if name.strip()]
#     car_numbers = get_car_numbers()
#     car_choices = [(name.strip(), name.strip()) for name in car_numbers if name.strip()]
#
#     SalesFormSet = formset_factory(
#         get_sales_form_class(dispatcher_choices, client_choices, car_choices),
#         extra=1
#     )
#
#     if request.method == 'POST':
#         formset = SalesFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 cleaned_data = form.cleaned_data
#                 dostavka = cleaned_data.get('dostavka')
#
#                 date_value = cleaned_data['date'].strftime('%Y-%m-%d')
#                 price_value = float(cleaned_data['price'])
#                 total_value = float(cleaned_data.get('total', 0))
#
#                 if dostavka == 'yes':
#                     # If "Доставка" is yes:
#                     # B: date
#                     # C: "Продажа услуга"
#                     # D: "Доставка"
#                     # E onwards: unit, price, currency, total, client, car_number
#                     data = [
#                         date_value,
#                         "Продажа услуга",
#                         "Доставка",
#                         int(cleaned_data['quantity']),
#                         cleaned_data['unit'],
#                         price_value,
#                         cleaned_data['currency'],
#                         total_value,
#                         cleaned_data['client'],
#
#                     ]
#                     append_to_nachislenie_sheet(data)
#                 else:
#                     # If "Доставка" is no, keep original format:
#                     # B: date, C: name, D: quantity, E: unit, F: price, G: currency,
#                     # H: total, I: client, J: car_number
#                     data = [
#                         '',
#                         date_value,
#                         cleaned_data['name'],
#                         int(cleaned_data['quantity']),
#                         cleaned_data['unit'],
#                         price_value,
#                         cleaned_data['currency'],
#                         total_value,
#                         cleaned_data['client'],
#                         cleaned_data['car_number'],
#                     ]
#                     append_to_sheet(data)
#
#             return render(request, 'sales/success.html')
#         else:
#             return render(request, 'sales/sales_entry.html', {'formset': formset})
#     else:
#         formset = SalesFormSet()
#         return render(request, 'sales/sales_entry.html', {'formset': formset})
#
#
# views.py

# sales/views.py

import logging
import io
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse

from xhtml2pdf import pisa

from .forms import SalesEntryForm
from .google_sheets import (
    append_to_sheet, append_to_nachislenie_sheet,
    get_dispatcher_names, get_client_names, get_car_numbers
)

logger = logging.getLogger(__name__)

def get_sales_form_class(dispatcher_choices, client_choices, car_choices):
    class CustomSalesEntryForm(SalesEntryForm):
        def __init__(self, *args, **kwargs):
            kwargs['dispatcher_choices'] = dispatcher_choices
            kwargs['client_choices'] = client_choices
            kwargs['car_choices'] = car_choices
            super().__init__(*args, **kwargs)
    return CustomSalesEntryForm


def sales_entry(request):
    dispatcher_names = get_dispatcher_names()
    dispatcher_choices = [(name.strip(), name.strip()) for name in dispatcher_names if name.strip()]
    client_names = get_client_names()
    client_choices = [(name.strip(), name.strip()) for name in client_names if name.strip()]
    car_numbers = get_car_numbers()
    car_choices = [(name.strip(), name.strip()) for name in car_numbers if name.strip()]

    SalesFormSet = formset_factory(
        get_sales_form_class(dispatcher_choices, client_choices, car_choices),
        extra=1
    )

    if request.method == 'POST':
        formset = SalesFormSet(request.POST)
        if formset.is_valid():
            sales_data_list = []
            for form in formset:
                cleaned_data = form.cleaned_data
                dostavka = cleaned_data['dostavka']
                date_value = cleaned_data['date'].strftime('%Y-%m-%d')
                price_value = float(cleaned_data['price'])
                total_value = float(cleaned_data['total'])

                # Write to Google Sheets
                if dostavka == 'yes':
                    data = [
                        date_value,
                        "Продажа услуга",
                        "Доставка",
                        int(cleaned_data['quantity']),
                        cleaned_data['unit'],
                        price_value,
                        cleaned_data['currency'],
                        total_value,
                        cleaned_data['client'],
                    ]
                    append_to_nachislenie_sheet(data)
                else:
                    data = [
                        '',
                        date_value,
                        cleaned_data['name'],
                        int(cleaned_data['quantity']),
                        cleaned_data['unit'],
                        price_value,
                        cleaned_data['currency'],
                        total_value,
                        cleaned_data['client'],
                        cleaned_data['car_number'],
                    ]
                    append_to_sheet(data)

                sales_data_list.append({
                    'date': date_value,
                    'name': cleaned_data['name'],
                    'quantity': int(cleaned_data['quantity']),
                    'unit': cleaned_data['unit'],
                    'price': price_value,
                    'currency': cleaned_data['currency'],
                    'total': total_value,
                    'client': cleaned_data['client'],
                    'car_number': cleaned_data['car_number'],
                    'dostavka': dostavka,
                })

            # Save sales_data_list in session for PDF
            request.session['sales_data'] = sales_data_list
            return redirect('sales-success')
        else:
            return render(request, 'sales/sales_entry.html', {'formset': formset})
    else:
        formset = SalesFormSet()
        return render(request, 'sales/sales_entry.html', {'formset': formset})


def sales_success(request):
    """
    Simple success page with a link to download PDF.
    """
    return render(request, 'sales/success.html')


# sales/views.py

import io
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse

from xhtml2pdf import pisa

from .forms import SalesEntryForm
from .google_sheets import (
    append_to_sheet, append_to_nachislenie_sheet,
    get_dispatcher_names, get_client_names, get_car_numbers
)

# sales/views.py

import io
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

from .forms import SalesEntryForm
from .google_sheets import (
    get_dispatcher_names, get_client_names, get_car_numbers
)
# sales/views.py

import os
import io
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

# sales/views.py

import os
from django.shortcuts import render

# sales/views.py

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register DejaVu Sans font for Cyrillic support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))


# sales/views.py

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register DejaVu Sans font for Cyrillic support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))


# sales/views.py

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from .models import SaleEntry  # Assuming you have a model for sales data

# Register DejaVu Sans font for Cyrillic support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))


# sales/views.py

from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register DejaVu Sans font for Cyrillic support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
import pytz


from datetime import datetime
import pytz
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register DejaVu Sans font for Cyrillic support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))


def sales_entry_pdf_view(request):
    # Retrieve data from session
    sales_data = request.session.get('sales_data', [])
    if not sales_data:
        return HttpResponse("No sales data found!", status=404)

    # Get the current date and time in Uzbekistan
    uzbekistan_tz = pytz.timezone("Asia/Tashkent")
    current_datetime = datetime.now(uzbekistan_tz).strftime("%Y-%m-%d %H:%M:%S")

    overall_total = sum(item['total'] for item in sales_data)
    last_item = sales_data[-1] if sales_data else None

    # Create an in-memory buffer for the PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Set the font
    pdf.setFont('DejaVuSans', 12)

    # Title
    pdf.drawString(200, 800, "Ch")

    # Header information

    pdf.drawString(400, 780, f"{current_datetime}")  # Uzbekistan date and time

    # Table header
    table_data = [
        ["Товар номи", "Куб (м³)", "Нархи", "Суммаси", "Доставка"]
    ]

    # Add sales data to the table
    for item in sales_data:
        table_data.append([
            item['name'],
            f"{item['quantity']} {item['unit']}",
            f"{item['price']} {item['currency']}",
            f"{item['total']}",
            "Доставка" if item['dostavka'] == 'yes' else "Нет"
        ])

    # Add total row
    table_data.append(["Жами", "", "", f"{overall_total}", ""])

    # Create the table
    table = Table(table_data, colWidths=[150, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Draw the table
    table.wrapOn(pdf, 50, 600)
    table.drawOn(pdf, 50, 600)

    # Footer information
    pdf.drawString(50, 450, f"Авто маркаси: __________________________")
    pdf.drawString(50, 430, f"Давлат рақами: {last_item['car_number'] if last_item else '________'}")
    pdf.drawString(50, 410, f"Имзо: __________________________________")

    # Finish the PDF
    pdf.showPage()
    pdf.save()

    # Get the PDF data from the buffer
    buffer.seek(0)
    pdf_data = buffer.getvalue()
    buffer.close()

    # Return the PDF as a download
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="uzbek_receipt.pdf"'
    return response


def convert_html_to_pdf(html_content):
    """
    Converts an HTML string to PDF using xhtml2pdf.
    """
    result = io.BytesIO()
    pdf = pisa.CreatePDF(
        src=html_content,
        dest=result,
        encoding='utf-8'
    )
    if not pdf.err:
        return result.getvalue()
    return None
