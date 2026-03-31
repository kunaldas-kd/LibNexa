from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from datetime import datetime
# import os
import Logics.database_connector as database_connector  # Your custom DB connector
import Logics.passedout as passedout
import Logics.total_amount_taking as total_amount_taking
import Logics.send_email as send_email
from pathlib import Path
# import database_connector 
# import passedout
# import total_amount_taking

# Add Footer to PDF
# ----------------- Auto Folder Setup in Documents -------------------
import os, sys
import ctypes.wintypes
import platform
import subprocess

def open_pdf(filepath):
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(filepath)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', filepath])
        else:  # Linux
            subprocess.run(['xdg-open', filepath])
    except Exception as e:
        print(f"Could not open PDF: {e}")

def get_desktop_path():
    CSIDL_DESKTOP = 0  # Desktop folder
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def select_output_folder():
    desktop = get_desktop_path()
    default_folder = os.path.join(desktop, "Library Clearance Certificate")
    os.makedirs(default_folder, exist_ok=True)
    return default_folder



# ----------------- Footer (Left Bottom) -------------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def add_footer(canvas, doc):
    page_width, _ = A4
    logo_width = 40
    footer_y = 0.2 * inch
    right_margin = 0.4 * inch
    spacing = 4  # spacing between logo and text
    text = "LibNest"

    canvas.saveState()
    try:
        # logo_path = os.path.join("IMG/logo.ico")
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # logo_path = os.path.join(base_dir, "LMS/IMG/logo2.png")
        logo_path = resource_path("IMG/logo2.png")
        # Set transparency if available
        if hasattr(canvas, "setFillAlpha"):
            canvas.setFillAlpha(0.8)
            canvas.setStrokeAlpha(0.8)

        # Set text properties
        canvas.setFont("Helvetica-Bold", 10)
        text_width = canvas.stringWidth(text, "Helvetica-Bold", 10)

        # Calculate starting X position so that logo + spacing + text ends at right margin
        logo_x = page_width - logo_width - spacing - text_width - right_margin
        text_x = logo_x + logo_width + spacing
        text_y = footer_y + logo_width / 2.5  # vertical center of logo

        # Draw logo
        if os.path.exists(logo_path):
            canvas.drawImage(
                logo_path,
                logo_x,
                footer_y,
                width=logo_width,
                height=logo_width,
                mask='auto',
                preserveAspectRatio=True
            )

        # Draw text to the right of logo
        canvas.drawString(text_x, text_y, text)

    except Exception as e:
        print(f"⚠️ Error in footer: {e}")
    finally:
        canvas.restoreState()


def Bodytext(cursor, student_name, Student_ID, department, institution_name, purpose):
    cursor.execute("SELECT `Payment Functionality` FROM users")
    amounts = cursor.fetchone()[0]
    if amounts == 1:
        body = f"""
            This is to certify that Mr./Ms. {student_name}, Registration No.: {Student_ID}, a student of {department} at {institution_name}, has returned all the books and other library materials borrowed from the {institution_name} Library.<br/><br/>
            As per the library records, there are no dues pending against his/her name.<br/><br/>
            This certificate is issued upon request for the purpose of {purpose}.<br/><br/>
            We wish him/her success in future endeavors.
        """
        return body
    else:
        body = f"""
            This is to certify that Mr./Ms. {student_name}, Registration No.: {Student_ID}, a student of {department} at {institution_name}, has returned all the books and other library materials borrowed from the {institution_name} Library.<br/><br/>
            
            This certificate is issued upon request for the purpose of {purpose}.<br/><br/>
            We wish him/her success in future endeavors.
        """
        return body

# ----------------- Certificate Number Generator -------------------
def generate_next_certificate_number(cursor, institutename, prefix="LIB"):
    cursor.execute('''SELECT SL_No FROM Passedout_Students''')
    student = cursor.fetchall()

    current_year = datetime.now().year
    short_name = institutename[:3].upper()

    if not student:
        next_serial = 1
    else:
        try:
            last_number = max(sl[0] for sl in student if isinstance(sl[0], int))
            next_serial = last_number + 1
        except ValueError:
            next_serial = 1

    certificate_no = f"{short_name}/{prefix}/{current_year}/{next_serial:04d}"
    print(certificate_no)
    return certificate_no


# ----------------- Generate Library Clearance PDF -------------------
def generate_library_clearance_certificate(cursor, Student_ID, student_name, department,
                                           institution_name, address, District, State, Country, Institute_Email,
                                           certificate_no, purpose, output_folder=None):

    institution_address = f"{address.title()}, {District.title()}, {State.title()}, {Country.title()}"

    if not output_folder:
        output_folder = select_output_folder()

    output_filename = f"library_clearance_certificate_{Student_ID}.pdf"
    output_filepath = os.path.join(output_folder, output_filename)

    doc = SimpleDocTemplate(output_filepath, pagesize=A4,
                            leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)

    styles = getSampleStyleSheet()
    center_style = ParagraphStyle(name="Center", parent=styles["Normal"], alignment=TA_CENTER)
    bold_center = ParagraphStyle(name="BoldCenter", parent=center_style, fontName="Helvetica-Bold", fontSize=14)
    normal_center = ParagraphStyle(name="NormalCenter", parent=center_style, fontSize=11)
    justify = ParagraphStyle(name="JustifiedIndented", parent=styles["Normal"], alignment=TA_JUSTIFY,
                             firstLineIndent=20)
    right_style = ParagraphStyle(name="RightAligned", parent=styles["Normal"], alignment=TA_RIGHT)

    elements = [
        Paragraph(institution_name, bold_center),
        Spacer(1, 0.06 * inch),
        Paragraph(institution_address, normal_center),
        Paragraph(f"Email: {Institute_Email.lower()}", normal_center),
        Spacer(1, 0.1 * inch),
        HRFlowable(width="100%", thickness=1, color="black"),
        Spacer(1, 0.3 * inch),
    ]

    date_today = datetime.today().strftime("%d/%m/%Y")
    cert_table = Table(
        [[f"Certificate No.: {certificate_no}", f"Date: {date_today}"]],
        colWidths=[3.5 * inch, 3.5 * inch]
    )
    cert_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(cert_table)
    elements.append(Spacer(1, 1.5 * inch))

    elements.append(Paragraph("Library Clearance Certificate", ParagraphStyle(
        name="CertTitle", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=13, alignment=TA_CENTER, spaceAfter=12
    )))

    body_text = Bodytext(cursor, student_name, Student_ID, department, institution_name, purpose)
    
    elements.append(Paragraph(body_text.strip(), justify))
    elements.append(Spacer(1, 1.3 * inch))
    elements.append(Paragraph("Librarian<br/>(Signature & Seal)", right_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph("Name: ____________________", right_style))
    elements.append(Spacer(1, 0.06 * inch))
    elements.append(Paragraph("Designation: _______________", right_style))
    elements.append(Spacer(1, 0.06 * inch))
    elements.append(Paragraph(f"Date: {date_today}", right_style))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"✅ Certificate saved at: {output_filepath}")
    return output_filepath


# ----------------- Get Institute Info from DB -------------------
def get_institute_info(id):
    connection = database_connector.connect_to_db("admin_interface")
    if connection is None:
        print("Failed to connect to the database.")
        return None
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM id_pass WHERE Id = %s''', (id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


# ----------------- Main Function to Generate and Store PDF -------------------
def get_library_clearance_certificate(id, StudentId):
    user_db_name = f"{id}_library_db"
    student = StudentId.upper()
    connection = database_connector.connect_to_db(user_db_name)
    if connection is None:
        print("❌ Failed to connect to database.")
        return False

    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM students WHERE Student_ID = %s''', (student,))
    student_info = cursor.fetchone()

    if not student_info:
        print("❌ Student not found.")
        cursor.close()
        connection.close()
        return False

    student_id = student_info[0]
    student_name = student_info[1]
    department = student_info[3]
    studentmail = student_info[4]
    institute_info = get_institute_info(id)
    if not institute_info:
        print("❌ Institute info not found.")
        return False
    Library_name=institute_info[1]
    institute_name = institute_info[2]
    institute_email = institute_info[3]
    address = institute_info[4]
    district = institute_info[5]
    state = institute_info[6]
    country = institute_info[7]

    certificate_no = generate_next_certificate_number(cursor, institute_name)
    pdf_path1 = generate_library_clearance_certificate(cursor,
        student_id, student_name, department, institute_name,
        address, district, state, country, institute_email,
        certificate_no, purpose="Final Semester Clearance"
    )
    
    if not pdf_path1:
        return False

    with open(pdf_path1, "rb") as file:
        pdf_data = file.read()
    mail = send_email.send_library_clearance_email_with_pdf(student,studentmail,student_name,Library_name,institute_email)
    if mail == False:
        return False
    passedout.passedout_student(user_db_name, StudentId, certificate_no, pdf_data)
    connection.commit()
    pdf_filename = f"library_clearance_certificate_{student}.pdf"
    one_drive_desktop = Path.home() / "OneDrive" / "Desktop"
    default_desktop = Path.home() / "Desktop"
    if one_drive_desktop.exists():
        desktop_path = str(one_drive_desktop)
    else:
        desktop_path = str(default_desktop)

    pdf_folder = os.path.join(desktop_path, "Library Clearance Certificate")
    os.makedirs(pdf_folder, exist_ok=True)  # Ensure folder exists

    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Assume you generate PDF here...
    # with open(pdf_path, 'wb') as f:
    #     f.write(b"%PDF-1.4\n%Dummy PDF for testing...\n")  # Placeholder content

    print(f"Certificate saved at: {pdf_path}")
    open_pdf(pdf_path)
    print("📥 PDF successfully stored in database.")
    cursor.close()
    connection.close()
    return True


# ----------------- Optional Validation Class -------------------
class Validation:
    def book_return_status(id, Student):
        user_db_name = f"{id}_library_db"
        connection = None
        try:
            connection = database_connector.connect_to_db(user_db_name)
            if connection is None:
                print("Failed to connect to the database.")
                return False

            cursor = connection.cursor()
            cursor.execute('''SELECT Borrow FROM borrowed_books WHERE Student_ID = %s''', (Student.upper(),))
            returnbook = cursor.fetchall()
            if any(1 in val for val in returnbook):
                print("⚠️ Return all borrowed books first.")
                return False
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        

    def book_return_status_for_teacher(id, teacher):
        user_db_name = f"{id}_library_db"
        connection = None
        try:
            connection = database_connector.connect_to_db(user_db_name)
            if connection is None:
                print("Failed to connect to the database.")
                return False

            cursor = connection.cursor()
            cursor.execute('''SELECT Borrow FROM teacher_borrowed_books WHERE Teacher_ID = %s''', (teacher.upper(),))
            returnbook = cursor.fetchall()
            if any(1 in val for val in returnbook):
                print("⚠️ Return all borrowed books first.")
                return False
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
# Example usage:
# get_library_clearance_certificate(389612, "sid1008")

def valid_payment(db_name, student_id):
    connection = database_connector.connect_to_db(db_name)
    if connection is None:
        print("Failed to connect to the database.")
        return  # Use buffered cursor
    cursor = connection.cursor()
    cursor.execute("SELECT `Payment Functionality` FROM users")
    amounts = cursor.fetchone()[0]
    if amounts == 1:
        amount = total_amount_taking.fatch_amount(db_name, student_id)
        print(amount)  
        if amount > 0:
            print(f"Student {student_id} is blocked due to non-payment.")
            # payment_API.open_payment_page()
            return False
        else:
            return True 
    else:
        return True
    

# =========================================================================================================


# ----------------- Select Output Folder -------------------
def select_output_folder1():
    desktop = get_desktop_path()
    folder = os.path.join(desktop, "Library Clearance Certificate (Teachers)")
    os.makedirs(folder, exist_ok=True)
    return folder



# ----------------- Certificate Body (Teacher) -------------------
def TeacherBodytext(teacher_name, Teacher_ID, department, designation, institution_name, purpose):
    body = f"""
        This is to certify that Mr./Ms. {teacher_name}, Employee ID: {Teacher_ID}, working as {designation} in the {department} department of {institution_name}, has returned all the books and other library materials borrowed from the {institution_name} Library.<br/><br/>
        As per the library records, there are no dues pending against his/her name.<br/><br/>
        This certificate is issued upon request for the purpose of {purpose}.<br/><br/>
        We wish him/her success in future endeavors.
    """
    return body

# ----------------- Generate Certificate Number -------------------
def generate_next_certificate_number1(t_id, institutename, prefix="LIBT"):
    current_year = datetime.now().year
    short_name = institutename[:3].upper()
    next_serial = t_id[:4]
    return f"{short_name}/{prefix}/{current_year}/{next_serial}"

# ----------------- PDF Generation -------------------
def generate_teacher_clearance_pdf1(cursor, Teacher_ID, teacher_name, department, designation,
                                   institution_name, address, District, State, Country, Institute_Email,
                                   certificate_no, purpose, output_folder=None):

    institution_address = f"{address.title()}, {District.title()}, {State.title()}, {Country.title()}"
    if not output_folder:
        output_folder = select_output_folder1()

    filename = f"teacher_clearance_certificate_{Teacher_ID}.pdf"
    filepath = os.path.join(output_folder, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)

    styles = getSampleStyleSheet()
    center_style = ParagraphStyle(name="Center", parent=styles["Normal"], alignment=TA_CENTER)
    bold_center = ParagraphStyle(name="BoldCenter", parent=center_style, fontName="Helvetica-Bold", fontSize=14)
    normal_center = ParagraphStyle(name="NormalCenter", parent=center_style, fontSize=11)
    justify = ParagraphStyle(name="Justified", parent=styles["Normal"], alignment=TA_JUSTIFY, firstLineIndent=20)
    right_style = ParagraphStyle(name="Right", parent=styles["Normal"], alignment=TA_RIGHT)

    date_today = datetime.today().strftime("%d/%m/%Y")
    elements = [
        Paragraph(institution_name, bold_center),
        Spacer(1, 0.06 * inch),
        Paragraph(institution_address, normal_center),
        Paragraph(f"Email: {Institute_Email.lower()}", normal_center),
        Spacer(1, 0.1 * inch),
        HRFlowable(width="100%", thickness=1),
        Spacer(1, 0.3 * inch),
        Table([[f"Certificate No.: {certificate_no}", f"Date: {date_today}"]],
              colWidths=[3.5 * inch, 3.5 * inch],
              style=[
                  ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                  ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                  ('FONTSIZE', (0, 0), (-1, -1), 11),
                  ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
              ]),
        Spacer(1, 1.5 * inch),
        Paragraph("Library Clearance Certificate", ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=13, alignment=TA_CENTER, spaceAfter=12)),
        Paragraph(TeacherBodytext(teacher_name, Teacher_ID, department, designation, institution_name, purpose), justify),
        Spacer(1, 1.3 * inch),
        Paragraph("Librarian<br/>(Signature & Seal)", right_style),
        Spacer(1, 0.2 * inch),
        Paragraph("Name: ____________________", right_style),
        Spacer(1, 0.06 * inch),
        Paragraph("Designation: _______________", right_style),
        Spacer(1, 0.06 * inch),
        Paragraph(f"Date: {date_today}", right_style),
    ]

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"✅ Certificate saved: {filepath}")
    return filepath

# ----------------- Institute Info -------------------
# def get_institute_info(id):
#     connection = database_connector.connect_to_db("admin_interface")
#     if connection is None:
#         print("❌ Could not connect to admin database.")
#         return None
#     cursor = connection.cursor()
#     cursor.execute('''SELECT * FROM id_pass WHERE Id = %s''', (id,))
#     result = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     return result

# ----------------- Main Function -------------------
def get_teacher_clearance_certificate1(id, TeacherId):
    user_db_name = f"{id}_library_db"
    teacher = TeacherId.upper()
    connection = database_connector.connect_to_db(user_db_name)
    if connection is None:
        print("❌ Failed to connect to database.")
        return False

    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM teachers WHERE Teacher_ID = %s''', (teacher,))
    teacher_info = cursor.fetchone()

    if not teacher_info:
        print("❌ Teacher not found.")
        cursor.close()
        connection.close()
        return False

    teacher_id = teacher_info[0]
    teacher_name = teacher_info[1]
    designation = teacher_info[2]
    department = teacher_info[3]
    email = teacher_info[4]

    institute_info = get_institute_info(id)
    if not institute_info:
        print("❌ Institute information not found.")
        cursor.close()
        connection.close()
        return False

    Library_name=institute_info[1]
    institute_name = institute_info[2]
    institute_email = institute_info[3]
    address = institute_info[4]
    district = institute_info[5]
    state = institute_info[6]
    country = institute_info[7]

    certificate_no = generate_next_certificate_number1(teacher_id, institute_name)
    pdf_path = generate_teacher_clearance_pdf1(
        cursor,
        teacher_id, teacher_name, department, designation,
        institute_name, address, district, state, country,
        institute_email, certificate_no, purpose="Faculty Resignation/Transfer"
    )
    mail = send_email.send_teacher_library_clearance_email_with_pdf(teacher, email, teacher_name, Library_name, institute_email)
    if mail == False:
        return False
    if not pdf_path:
        return False

    cursor.execute('''UPDATE teachers SET Employment_Status = 'EX-TEACHER' WHERE Teacher_ID = %s''',(teacher,))
    connection.commit()
    pdf_filename = f"teacher_clearance_certificate_{TeacherId}.pdf"
    one_drive_desktop = Path.home() / "OneDrive" / "Desktop"
    default_desktop = Path.home() / "Desktop"
    if one_drive_desktop.exists():
        desktop_path = str(one_drive_desktop)
    else:
        desktop_path = str(default_desktop)

    pdf_folder = os.path.join(desktop_path, "Library Clearance Certificate (Teachers)")
    os.makedirs(pdf_folder, exist_ok=True)  # Ensure folder exists

    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Assume you generate PDF here...
    # with open(pdf_path, 'wb') as f:
    #     f.write(b"%PDF-1.4\n%Dummy PDF for testing...\n")  # Placeholder content

    print(f"Certificate saved at: {pdf_path}")
    open_pdf(pdf_path)
    print("📥 Teacher certificate generated successfully.")
    cursor.close()
    connection.close()
    return True

# Example usage:
# get_teacher_clearance_certificate1(389612, "T003")





# def student_library_clearance_certificate(student_id):
    