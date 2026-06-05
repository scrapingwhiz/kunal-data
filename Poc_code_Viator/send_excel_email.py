import smtplib
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import pandas as pd
import datetime
from config_data import *
today = today_date.strftime("%Y_%m_%d")

def send_mail(temp_mail = False):

    # === Email Settings ===
    smtp_server = "smtp.hostinger.com"  # or your SMTP server
    smtp_port = 587
    sender_email = "delivery-alerts@xwiz.io"
    password = "K(d@@%wT'3],U+'QN9S~PQZCh"  # use App Password for Gmail

    # Define recipients
    if temp_mail:
        print("Sending Temp Mail....")
        to_emails = ["dev21.ultroneous@gmail.com"]
        cc_emails = ["dev11.ultroneous@gmail.com"]
        bcc_emails = ["avhinandan.ultroneous@gmail.com"]
    else:
        print("Sending Client Mail....")
        to_emails = ["Gaurav.Mitkar@eclerx.com", "HBD_Quality@eclerx.com"]
        cc_emails = ["gaurav@ultroneous.com"]
        bcc_emails = ["dev21.ultroneous@gmail.com", 'dev11.ultroneous@gmail.com', 'avhinandan.ultroneous@gmail.com']


    all_recipients = to_emails + cc_emails + bcc_emails
    # === File Path ===
    file_name = f'XWIZ_Viator_Output_{today}.xlsx'
    excel_file_path = os.path.join(excel_dir,file_name)

    # === Count rows from Excel ===
    df = pd.read_excel(excel_file_path)
    delivered_count = len(df)   # row count
    subject_date = today_date.strftime("%d-%b-%Y")  # Example: 29-Sep-2025
    subject = f"[XWIZ Delivery Alert] Viator Daily Delivery Report - {subject_date}"
    # === Create HTML Report ===
    date = today_date.strftime("%Y-%m-%d")
    date1 = today_date.strftime("%d-%b-%Y")

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #1a1a1a;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        thead {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
        }}
        th, td {{
            padding: 15px;
            font-size: 0.9rem;
        }}
        tbody tr {{
            border-bottom: 1px solid #dee2e6;
        }}
        tbody tr:hover {{
            background: #f8fafc;
        }}
        .status-success {{
            background: #dcfce7;
            color: #166534;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>File Delivery Report</h1>
                <p>Summary of latest Viator data delivery</p>
            </div>
            <div class="files-section">
                <h2>Delivered Files</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Region</th>
                            <th>Platform</th>
                            <th>Delivered Count</th>
                            <th>Status</th>
                            <th>File Path</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- 📅 DATE ROW -->
                        <tr style="background-color: #f8f9fa;">
                            <td colspan="6" style="padding: 12px; font-weight: bold; color: #495057; border-bottom: 1px solid #dee2e6;">
                                📅 {date}
                            </td>
                        </tr>
                        <!-- FILE ROW -->
                        <tr>
                            <td>Multi-Region</td>
                            <td>Viator</td>
                            <td>{delivered_count}</td>
                            <td><span class="status-success">✓ Delivered</span></td>
                            <td>File Attached in this Email</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    # === Create email message ===
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_emails)
    msg["Cc"] = ", ".join(cc_emails)
    msg["Bcc"] = ", ".join(bcc_emails)
    msg["Subject"] = f"[XWIZ Delivery Alert] Viator Daily Delivery Report - {date1}"

    # Attach the HTML body
    msg.attach(MIMEText(html_template, "html"))
    zip_filename = f"json_pages_{today}.zip"
    zip_path = os.path.join(save_dir, zip_filename)

    with open(zip_path, "rb") as attachment:
        part = MIMEBase("application", "zip")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={zip_filename}")
    msg.attach(part)
    # Attach the Excel file
    with open(excel_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={file_name}")
    msg.attach(part)

    # === Send email ===
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, all_recipients, msg.as_string())
        print(f"✅ Email sent successfully with attachment {file_name} and row count {delivered_count}")
    except Exception as e:
        print("❌ Error sending email:", e)