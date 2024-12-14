from sales.google_sheets import append_to_sheet

if __name__ == '__main__':
    test_data = [
        '2024-12-13',  # Date
        'Product A',   # Name
        10,            # Quantity
        'kg',          # Unit
        25.50,         # Price
        'USD',         # Currency
        255.00,        # Total
        'Client X',    # Client
        '123ABC',      # Car Number
        1.0,           # Exchange Rate
        255.00         # Total in USD
    ]

    try:
        response = append_to_sheet(test_data)
        print("Google Sheets API Response:", response)
    except Exception as e:
        print(f"Error: {e}")
