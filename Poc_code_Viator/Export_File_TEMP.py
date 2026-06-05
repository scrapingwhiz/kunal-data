import os.path
import time

import pandas as pd

from Vietor_QA_Check import main
from config_data import *
from send_excel_email import send_mail


def Export_File():

    data = list(product_data.find({}).limit(1000000))
    df = pd.DataFrame(data)
    try:
        df.pop('_id')
        if len(df) < 1000:
            raise Exception("Data rows should not be less then 1k...")
    except Exception as e:
        print("Getting blank data in dataframe....", e)
        sys.exit(5)

    # Specify the columns you want to export
    columns_to_export =[
        "Order",
    "Customer Market",
    "Customer Market Key",
    "Region",
    "Destination Code",
    "Destination",
    "Service Name",
    "Service code",
    "Modality Name",
    "Modality Code",
    "Modality Order",
    "Company",
    "Min pax",
    "Booking in advance",
    "Search date",
    "Calender Week",
    "Arrival date",
    "Available Arrival date",
    "Price",
    "Currency",
    "Deliverable Date",
    "Contract Info",
    "Incomming Office Code",
    "Transfers- extracted info",
    "Transfers - options",
    "Pick up point- extracted info",
    "Pick up point- options",
    "Drop off -extracted info",
    "Drop off -options",
    "Meals - extracted info",
    "Meals : included/ excluded",
    "Start Time",
    "End Time",
    "Duration",
    "Segmentation-duration",
    "Assistance/guided-extracted info",
    "Assistance/guided",
    "Language -extracted info",
    "Promotion Description",
    "Promotion",
    "Supplier",
    "Links",
    "Modality Availability",
    "Tool Tip",
    "Review",
    "opiniones",
    "Cancelaciones",
    "Mobile Data Information",
    "Contractor",
    "Product Line",
    "Scope"
    ]

    MARKET_TO_CURRENCY = {
        "US": "USD",
        "UK": "GBP",
        "ES": "EUR",
        "IN": "INR",
        "PH": "PHP",
        "ZA": "ZAR",
        "AU": "AUD",
        "CA": "CAD",
        "MX": "MXN"
    }

    FX_RATES = {
        "USD": {
            "GBP": 0.79,
            "EUR": 0.92,
            "INR": 83.1,
            "PHP": 56.0,
            "ZAR": 18.6
        }
    }

    def convert_price(row):
        base_currency = row["Currency"]
        market = row["Customer Market Key"]

        target_currency = MARKET_TO_CURRENCY.get(market)

        if not target_currency:
            return None, None, "NO_MARKET_MAPPING"

        if base_currency == target_currency:
            return row["Price"], target_currency, "NO_CONVERSION"

        if base_currency != "USD":
            return None, target_currency, "UNSUPPORTED_BASE"

        rate = FX_RATES["USD"].get(target_currency)
        if not rate:
            return None, target_currency, "FX_RATE_MISSING"

        converted = round(row["Price"] * rate, 2)
        return converted, target_currency, "FX_CONVERTED"

    df[[
        "Converted Price",
        "Converted Currency",
        "Conversion Method"
    ]] = df.apply(
        lambda r: pd.Series(convert_price(r)),
        axis=1
    )
    columns = [
        "Links",
        "Arrival date",
        "Currency",
        "Customer Market Key",
        "Customer Market",
        "Price",
        "Converted Price",
        "Converted Currency",
        "Conversion Method"
    ]
    df1 = df[columns]
    df1.to_excel(f'XWIZ_Viator_Output_{today}.xlsx', index=False,
                engine_kwargs={"options": {'strings_to_numbers': True, 'strings_to_urls': False}})
    print(f"Excel file saved to {f'XWIZ_Viator_Output_{today}.xlsx'}")

    df = df[columns_to_export]

    excel_file_path = os.path.join(excel_dir, f'XWIZ_Viator_Output_{today}.xlsx')

    df.to_excel(excel_file_path, index=False, engine_kwargs={"options": {'strings_to_numbers': True, 'strings_to_urls': False}})
    print(f"Excel file saved to {excel_file_path}")

    qa_results, data_summary, html_report = main(df, excel_dir)
    if not qa_results:
        print("Please Check QA Report and Solve Data Quality Issues First....")
        return

if __name__ == '__main__':
    Export_File()