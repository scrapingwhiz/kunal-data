import os.path
import time
import zipfile

import pandas as pd

from Vietor_QA_Check import main
from config_data import *
from send_excel_email import send_mail


def Export_File():

    data = list(product_data.find({}).limit(1000000))
    df = pd.DataFrame(data)
    try:
        df.pop('_id')
        if len(df) < 900:
            raise Exception("Data rows should not be less then 1k...")
    except Exception as e:
        print("Getting blank data in dataframe....", e)
        sys.exit(5)

    # Specify the columns you want to export
    # Specify the columns you want to export
    columns_to_export = [
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
        "Scope",
        "file_name"
    ]

    df.rename(columns={'josn_file_path': 'file_name'}, inplace=True)

    def split_filename(filename):
        s = filename.split('\\')[-1]
        return s

    df['file_name'] = df['file_name'].apply(split_filename)

    df = df[columns_to_export]

    excel_file_path = os.path.join(excel_dir, f'XWIZ_Viator_Output_{today}.xlsx')

    df.to_excel(excel_file_path, index=False, engine_kwargs={"options": {'strings_to_numbers': True, 'strings_to_urls': False}})
    print(f"Excel file saved to {excel_file_path}")
    zip_filename = f"json_pages_{today}.zip"
    zip_path = os.path.join(save_dir, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(save_dir):
            if file.endswith(".json"):
                file_path = os.path.join(save_dir, file)
                zipf.write(file_path, arcname=file)

    print(f"JSON ZIP file saved to {zip_path}")
    qa_results, data_summary, html_report = main(df, excel_dir)
    if not qa_results:
        print("Please Check QA Report and Solve Data Quality Issues First....")
        return

    send_mail(temp_mail=False)

if __name__ == '__main__':
    Export_File()