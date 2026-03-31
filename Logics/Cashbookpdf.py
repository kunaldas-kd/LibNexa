from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from datetime import datetime
import os
import re
import pandas as pd
import Logics.database_connector as database_connector


def generate_cash_transactions_pdf(data, Start_Date=None, End_Date=None, filename=None):
    
    db_name = "admin_interface"
    connection = None

    try:
        connection = database_connector.connect_to_db(db_name)
        if not connection:
            print("❌ Failed to connect to the database.")
            return False

        cursor = connection.cursor()
        cursor.execute("""SELECT Institute_name, Institute_Email, Address, District, Country FROM id_pass""")
        result = cursor.fetchone()
        if not result:
            print("❌ No institute info found.")
            return False

        institute_name, institute_email, address, district, country = result
        full_address = f"{address}, {district}, {country}"

        # Convert to DataFrame
        headers = ["Transaction_Id", "Student_Id", "Transaction_Date",
                   "Description", "Transaction_Type", "Amount", "Credit", "Debit", "Balance"]
        df = pd.DataFrame(data, columns=headers)
        df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"], errors="coerce")

        # Filter by date range
        if Start_Date:
            Start_Date = pd.to_datetime(Start_Date)
            df = df[df["Transaction_Date"] >= Start_Date]
        if End_Date:
            End_Date = pd.to_datetime(End_Date)
            df = df[df["Transaction_Date"] <= End_Date]

        df["Transaction_Date"] = df["Transaction_Date"].dt.strftime('%d-%m-%Y')
        # Convert Credit and Debit 1 → ✔️, else empty
        for col in ["Credit", "Debit"]:
            df[col] = df[col].apply(lambda x: "✔️" if str(x).strip() == "1" else "")
            df[col] = df[col].astype(str).str.replace(r'[^\u2714]', '', regex=True)

        # Auto filename
        if not filename:
            if Start_Date and End_Date:
                filename = f"Cash Transactions {Start_Date.strftime('%d-%m-%Y')} to {End_Date.strftime('%d-%m-%Y')}.pdf"
            elif Start_Date:
                filename = f"Cash Transactions from {Start_Date.strftime('%d-%m-%Y')}.pdf"
            elif End_Date:
                filename = f"Cash Transactions till {End_Date.strftime('%d-%m-%Y')}.pdf"
            else:
                filename = "Cash_Transactions_Report.pdf"

        filename = re.sub(r'[\\/*?:"<>|()\s]+', '_', filename)

        # Output path
        output_folder = os.path.expanduser("~/Downloads")
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)

        # Handle locked file
        counter = 1
        while os.path.exists(filepath):
            try:
                with open(filepath, 'a'):
                    break
            except PermissionError:
                filepath = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{counter}.pdf")
                counter += 1

        # PDF setup
        doc = SimpleDocTemplate(
            filepath,
            pagesize=landscape(A4),
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch
        )

        # Styles
        styles = getSampleStyleSheet()
        center_bold = ParagraphStyle(
            name="CenterBold", parent=styles["Normal"],
            alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=14
        )
        center_normal = ParagraphStyle(
            name="CenterNormal", parent=styles["Normal"],
            alignment=TA_CENTER, fontSize=11
        )
        cell_style = ParagraphStyle(
            name="CellStyle", parent=styles["Normal"],
            alignment=TA_LEFT, fontSize=8, leading=10
        )

        # Header section
        elements = [
            Paragraph(institute_name.upper(), center_bold),
            Spacer(1, 0.06 * inch),
            # Paragraph("Library Department", center_normal),
            Paragraph(full_address, center_normal),
            Paragraph(f"Email: {institute_email}", center_normal),
            Spacer(1, 0.1 * inch),
            HRFlowable(width="100%", thickness=1, color="black"),
            Spacer(1, 0.15 * inch),
            Paragraph("Cash Transactions Report", center_bold),
            Spacer(1, 0.1 * inch),
            Paragraph(f"Date Range: {Start_Date.strftime('%d-%m-%Y') if Start_Date else '...'} "
                      f"to {End_Date.strftime('%d-%m-%Y') if End_Date else '...'}", center_normal),
            Spacer(1, 0.2 * inch)
        ]

        # Wrap text
# Wrap each cell properly
        def wrap(val, col_name=None):
            if col_name == "Transaction_Date":
                try:
                    return Paragraph(str(val), cell_style)
                except:
                    return Paragraph("--", cell_style)
            return Paragraph(str(val), cell_style)

        table_data = [headers] + [[wrap(v, headers[i]) for i, v in enumerate(row)] for row in df.values.tolist()]

        # Calculate flexible column widths (fit to available page width)
        total_page_width = landscape(A4)[0] - (0.5 * inch + 0.5 * inch)  # full width minus margins
        col_count = len(headers)
        col_widths = [total_page_width / col_count] * col_count  # equal distribution (or you can customize ratios)

        # Create table
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), "#cacaca"),
            ('GRID', (0, 0), (-1, -1), 0.5, 'black'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        elements.append(table)
        doc.build(elements)

        print(f"✅ PDF saved (auto-fit to page) at: {filepath}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    finally:
        if connection:
            connection.close()
