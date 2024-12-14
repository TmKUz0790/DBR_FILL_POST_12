
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal objects to float
        return super().default(obj)


from django.shortcuts import render
from .forms import SalesEntryForm
from .google_sheets import append_to_sheet, get_dispatcher_names, get_client_names
from datetime import date
import logging

# Configure logging
from django.shortcuts import render
from .forms import SalesEntryForm
from .google_sheets import append_to_sheet, get_dispatcher_names, get_client_names,get_car_numbers
from datetime import date
import logging

# Configure logging
logger = logging.getLogger(__name__)

def sales_entry(request):
    dispatcher_names = get_dispatcher_names()
    dispatcher_choices = [(name.strip(), name.strip()) for name in dispatcher_names if name.strip()]
    client_names = get_client_names()
    client_choices = [(name.strip(), name.strip()) for name in client_names if name.strip()]
    car_numbers = get_car_numbers()
    car_choices = [(name.strip(), name.strip()) for name in car_numbers if name.strip()]

    if request.method == 'POST':
        # Make sure all arguments are passed as keywords to avoid positional conflicts
        form = SalesEntryForm(data=request.POST, dispatcher_choices=dispatcher_choices, client_choices=client_choices, car_choices=car_choices)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                data = [
                    '',
                    cleaned_data['date'].strftime('%Y-%m-%d'),
                    cleaned_data['name'],
                    int(cleaned_data['quantity']),
                    cleaned_data['unit'],
                    float(cleaned_data['price']),
                    cleaned_data['currency'],
                    float(cleaned_data.get('total', 0)),  # Default if None
                    cleaned_data['client'],
                    cleaned_data['car_number'],
                    # float(cleaned_data.get('rate', 1)),  # Default if None
                    # float(cleaned_data.get('total_usd', 0))  # Default if None
                ]
                append_to_sheet(data)
                return render(request, 'sales/success.html')
            except Exception as e:
                logger.error(f"Error writing to Google Sheets: {str(e)}")
                return render(request, 'sales/error.html', {'error': str(e)})
        else:
            return render(request, 'sales/sales_entry.html', {'form': form})
    else:
        # Also, pass dispatcher and client choices as keyword arguments here
        form = SalesEntryForm(dispatcher_choices=dispatcher_choices, client_choices=client_choices,car_choices=car_choices)
        return render(request, 'sales/sales_entry.html', {'form': form})
