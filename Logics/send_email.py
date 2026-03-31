import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from email.mime.base import MIMEBase
from email import encoders
import os
from pathlib import Path
    
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_email(to_email, Id, password, Name):
    """Sends an email with the user ID and password."""
    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"  
    subject = "Your LibNexa Credentials"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear {Name},</p>
        <p>Welcome to <strong>LibNexa</strong> – your digital library platform.</p>
        <p>Here are your access details:</p>
        <table style="border-collapse: collapse;">
            <tr><td style="padding: 4px;"><strong>ID:</strong></td><td style="padding: 4px;">{Id}</td></tr>
            <tr><td style="padding: 4px;"><strong>Password:</strong></td><td style="padding: 4px;">{password}</td></tr>
        </table>
        <p>We recommend you change your password after your first login.</p>
        <p>If you did not request this account, please ignore this message or contact us at <a href="mailto:nestivetech@gmail.com">support</a>.</p>
        <br>
        <p>Regards,<br>Nestive Tech<br><a href="mailto:nestivetech@gmail.com">LibNexa Support</a></p>
        <hr>
        <small>This is an automated message from LibNexa. Please do not reply directly to this email.</small>
    </body>
    </html>
    """

    text_content = f"""
    Dear {Name},

    Welcome to LibNexa – your digital library platform.

    Here are your access details:
    --------------------------------------
    ID: {Id}
    Password: {password}
    --------------------------------------

    Please change your password after first login.

    If you did not request this account, please ignore this message or contact us at nestivetech@gmail.com.

    Regards,
    Nestive Tech
    LibNexa Support <nestivetech@gmail.com>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = "LibNexa<nestivetech@gmail.com>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email}")
        return True
      
    except Exception as e:
        logging.error(f"Failed to send email in send_email(send_email): {e}")
     

def send_reminder_email_1(to_email, recipient_name, book_title, amount, library, Contact):
    """Sends an email with the user ID and password."""
    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"  
    

    subject = "Friendly Reminder: Upcoming Due Date"

    # Email content for one book
    # HTML content
    html_content = f"""
            <html>
            <body>
            <p>Dear {recipient_name},</p>
            <p>This is a friendly reminder that the book <strong>{book_title}</strong> borrowed from our library is due soon.</p>
            <p>We kindly request that you return it on time to avoid any late fees or penalties. If you have already returned it, please ignore this message.</p>
            <p>Please note that a fee of <strong>{amount}</strong> will be charged per day after 3 days past the due date.</p>
            <p>Should you need an extension or assistance, don’t hesitate to contact us at <a href='mailto:{Contact}'>{library.title()} Support</a>.</p>
            <p>Thank you for your attention to this matter, and we look forward to serving you again soon!</p>
            <p>Best regards,<br>Librarian<br>{library}<br><a href="mailto:{Contact}">{library.title()} Support</a></p>
            </body>
            </html>
            """

    # Plain text content
    text_content = f"""
            Dear {recipient_name},

            This is a friendly reminder that the book '{book_title}' borrowed from our library is due soon.

            We kindly request that you return it on time to avoid any late fees or penalties. If you have already returned it, please ignore this message.

            Please note that a fee of {amount} will be charged per day after 3 days past the due date.

            Should you need an extension or assistance, don’t hesitate to contact us at {Contact}.

            Thank you for your attention to this matter, and we look forward to serving you again soon!

            Best regards,
            Librarian
            {library}
            {Contact}
            """

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{library}<nestivetech@gmail.com>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email in send_email(end_reminder_email): {e}")
        return False

def send_reminder_email_2(to_email, recipient_name, book_title, amount, return_date, library, Contact):
    """Sends an email with the user ID and password."""
    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"  
    

    subject = "Renewal Deadline Missed – Penalty Period Begins"

    # Email content for one book
    # HTML content
    html_content = f"""
            <html>
                <body>
                    <p>Dear {recipient_name},</p>
                    <p>This is a reminder that the renewal deadline for the book <strong>{book_title}</strong> was <strong>{return_date}</strong>, and it has not yet been renewed or returned.</p>
                    <p>As of today, a penalty of <strong>{amount}</strong> per day will begin to apply, as per our library policy.</p>
                    <p>We kindly request that you return the book as soon as possible to minimize additional charges.</p>
                    <p>For any assistance or to request an extension, feel free to contact us at <a href="mailto:{Contact}">{library.title()} Support</a>.</p>
                    <p>Thank you for your prompt attention.</p>
                    <p>Best regards,<br>Librarian<br>{library}<br><a href="mailto:{Contact}">{library.title()} Support</a></p>
                </body>
            </html>
            """

    # Plain text content
    text_content = f"""
            Dear {recipient_name},
            This is a reminder that the renewal deadline for the book '{book_title}' was {return_date}, and it has not yet been renewed or returned.
            As of today, a penalty of {amount} per day will begin to apply, as per our library policy.
            We kindly request that you return the book as soon as possible to minimize additional charges.
            For any assistance or to request an extension, feel free to contact us at {library} Support.
            Thank you for your prompt attention.
            Best regards,
            Librarian
            {library}
            {library} Support
            """

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{library}<nestivetech@gmail.com>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email in send_email(end_reminder_email): {e}")
        return False
    

def send_otp_email(to_email, recipient_name, otp_code):
    """
    Sends an OTP email to the user for identity verification.
    """
    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"
    subject = "LibNexa OTP Verification – Action Required"

    # HTML version of the email
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear {recipient_name},</p>
        <p>We received a request to verify your identity for accessing or updating your <strong>LibNexa</strong> account.</p>
        <p>Please use the following One-Time Password (OTP) to proceed:</p>
        <h2 style="color: #2E86C1;">{otp_code}</h2>
        <p>This OTP is valid for <strong>5 minutes</strong>. Please do not share this code with anyone.</p>
        <p>If you did not request this, please ignore this email or contact us at 
        <a href="mailto:{sender_email}">LibNexa Support</a>.</p>
        <br>
        <p>Regards,<br>Nestive Tech<br><a href="mailto:{sender_email}">LibNexa Support</a></p>
        <hr>
        <small>This is an automated message from LibNexa. Please do not reply directly to this email.</small>
    </body>
    </html>
    """

    # Plain-text version
    text_content = f"""
    Dear {recipient_name},

    We received a request to verify your identity for accessing or updating your LibNexa account.

    Please use the following One-Time Password (OTP) to proceed:

    OTP: {otp_code}

    This OTP is valid for 5 minutes. Do not share this code with anyone.

    If you did not request this, please ignore this email or contact us at {sender_email}.

    Regards,
    Nestive Tech
    LibNexa Support <{sender_email}>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = f"LibNexa <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"OTP email sent successfully to {to_email}")
        return True

    except Exception as e:
        logging.error(f"Failed to send OTP email in send_otp_email(): {e}")
        return False

# ===================================================================================================
def send_library_clearance_email_with_pdf(studentid, to_email, recipient_name, library, contact_email):
    """Sends a library clearance email with attached PDF based on student ID."""
    

    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"

    subject = "Library Clearance Notification"

    # Construct the PDF path from Desktop
    one_drive_desktop = Path.home() / "OneDrive" / "Desktop"
    default_desktop = Path.home() / "Desktop"

    # Use OneDrive/Desktop if it exists, else fallback to standard Desktop
    if one_drive_desktop.exists():
        desktop_path = str(one_drive_desktop)
    else:
        desktop_path = str(default_desktop)
    pdf_folder = os.path.join(desktop_path, "Library Clearance Certificate")
    pdf_filename = f"library_clearance_certificate_{studentid}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # HTML content
    html_content = f"""
        <html>
            <body>
                <p>Dear {recipient_name},</p>
                <p>We hope this message finds you well.</p>
                <p>This is to inform you that your <strong>Library Clearance</strong> is now due as part of the institutional formalities.</p>
                <p>Please ensure that all borrowed books are returned and any dues are cleared. Once completed, you may collect your <strong>Library Clearance Certificate</strong>.</p>
                <p>We have attached your clearance certificate for your reference.</p>
                <p>If you have already completed the process, kindly ignore this message.</p>
                <p>For any assistance, feel free to contact us at <a href="mailto:{contact_email}">{library} Support</a>.</p>
                <p>Best regards,<br>
                Librarian<br>
                {library}<br>
                <a href="mailto:{contact_email}">{library} Support</a></p>
            </body>
        </html>
    """

    # Plain text version
    text_content = f"""
        Dear {recipient_name},

        We hope this message finds you well.

        This is to inform you that your Library Clearance is now due as part of the institutional formalities.
        Please ensure that all borrowed books are returned and any dues are cleared. Once completed, you may collect your Library Clearance Certificate.

        We have attached your clearance certificate for your reference.

        If you have already completed the process, kindly ignore this message.

        For any assistance, feel free to contact us at {library} Support ({contact_email}).

        Best regards,
        Librarian
        {library}
        {library} Support
    """

    msg = MIMEMultipart("mixed")
    msg["From"] = f"{library} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    # msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    # Attach the PDF file
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
            msg.attach(part)
    else:
        logging.warning(f"PDF not found for student ID {studentid}: {pdf_path}")
        return False

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Clearance email sent to {to_email} with attachment.")
        return True
    except Exception as e:
        logging.error(f"Failed to send clearance email: {e}")
        return False


def send_teacher_library_clearance_email_with_pdf(teacherid, to_email, recipient_name, library, contact_email):
    """Sends a library clearance email with attached PDF to a teacher based on teacher ID."""

    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"

    subject = "Library Clearance Notification"

    # Construct the PDF path from Desktop (supports OneDrive or default)
    one_drive_desktop = Path.home() / "OneDrive" / "Desktop"
    default_desktop = Path.home() / "Desktop"

    # Use OneDrive/Desktop if it exists, else fallback to standard Desktop
    if one_drive_desktop.exists():
        desktop_path = str(one_drive_desktop)
    else:
        desktop_path = str(default_desktop)

    # Continue building the rest of the path
    pdf_folder = os.path.join(desktop_path, "Library Clearance Certificate (Teachers)")
    pdf_filename = f"teacher_clearance_certificate_{teacherid}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # HTML email content
    html_content = f"""
        <html>
            <body>
                <p>Dear Prof. {recipient_name},</p>
                <p>We hope this message finds you well.</p>
                <p>This is to inform you that your <strong>Library Clearance</strong> is now due as part of the institutional formalities.</p>
                <p>Please ensure that all borrowed materials are returned. Once completed, you may collect your <strong>Library Clearance Certificate</strong>.</p>
                <p>We have attached your clearance certificate for your reference.</p>
                <p>If you have already completed the process, kindly ignore this message.</p>
                <p>For any assistance, feel free to contact us at <a href="mailto:{contact_email}">{library} Support</a>.</p>
                <p>Best regards,<br>
                Librarian<br>
                {library}<br>
                <a href="mailto:{contact_email}">{library} Support</a></p>
            </body>
        </html>
    """

    # Plain text email content
    text_content = f"""
        Dear Prof. {recipient_name},

        We hope this message finds you well.

        This is to inform you that your Library Clearance is now due as part of the institutional formalities.
        Please ensure that all borrowed materials are returned. Once completed, you may collect your Library Clearance Certificate.

        We have attached your clearance certificate for your reference.

        If you have already completed the process, kindly ignore this message.

        For any assistance, feel free to contact us at {library} Support ({contact_email}).

        Best regards,
        Librarian
        {library}
        {library} Support
    """

    # Create the email message
    msg = MIMEMultipart("mixed")
    msg["From"] = f"{library} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    # msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    # Attach the PDF if it exists
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={pdf_filename}")
            msg.attach(part)
    else:
        logging.warning(f"PDF not found for teacher ID {teacherid}: {pdf_path}")
        return False

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Clearance email sent to {to_email} with attachment.")
        return True
    except Exception as e:
        logging.error(f"Failed to send clearance email: {e}")
        return False
    

    

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import logging

def send_library_email(cursor, studentid, book_id,  purpose, extra_info=None):
   
    cursor.execute("SELECT * FROM students WHERE Student_ID = %s",(studentid,))
    student_info=cursor.fetchone()
    to_email =student_info[4]
    recipient_name=student_info[1]
    
    cursor.execute("SELECT Book_Name FROM books WHERE Book_ID = %s", (book_id,))
    book_title = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM USERS")
    institute_info=cursor.fetchone()
    library =institute_info[1]
    Contact =institute_info[3]
    sender_email = "nestivetech@gmail.com"
    sender_password = "yqeb ecoe qtjq ykxz"  

    # Choose subject & body content based on purpose
    if purpose == "issue":
        subject = "Book Issue Confirmation"
        action_line = f"The book <strong>{book_title}</strong> has been successfully issued to you."
        extra_line = f"Please ensure to return it by <strong>{extra_info}</strong> to avoid late fees." if extra_info else ""
    elif purpose == "renew":
        subject = "Book Renewal Confirmation"
        action_line = f"The book <strong>{book_title}</strong> has been successfully renewed."
        extra_line = f"Your new due date is <strong>{extra_info}</strong>. Please ensure timely return to avoid charges." if extra_info else ""
    elif purpose == "submit":
        subject = "Book Submission Confirmation"
        action_line = f"The book <strong>{book_title}</strong> has been successfully returned."
        extra_line = "Thank you for returning the book on time!"
    else:
        logging.error(f"Invalid purpose: {purpose}")
        return False

    # HTML content
    html_content = f"""
        <html>
        <body>
        <p>Dear {recipient_name},</p>
        <p>{action_line}</p>
        <p>{extra_line}</p>
        <p>If you have any questions or need assistance, feel free to contact us at 
        <a href='mailto:{Contact}'>{library.title()} Support</a>.</p>
        <p>Best regards,<br>Librarian<br>{library}<br>
        <a href="mailto:{Contact}">{library.title()} Support</a></p>
        </body>
        </html>
    """

    # Plain text content
    text_content = f"""
        Dear {recipient_name},

        {action_line.replace('<strong>', '').replace('</strong>', '')}
        {extra_line.replace('<strong>', '').replace('</strong>', '')}

        If you have any questions or need assistance, contact us at {Contact}.

        Best regards,
        Librarian
        {library}
        {Contact}
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{library} <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logging.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email in send_library_email: {e}")
        return False



# send_email("kunaldas532001@outlook.com","564123","564123", "ashim")
# send_reminder_email_1("kunaldas532001@outlook.com", "kd", "app", "6", "falpol2", "kunaldas532001@gmail.com")
# send_reminder_email_2("kunaldas532001@outlook.com", "kd", "app", "6", "3-2-2025","falpol2", "kunaldas532001@gmail.com")
# send_otp_email("kunaldas532001@outlook.com", "Kd", 865325)
# send_library_clearance_email_with_pdf("SID1025", "kunaldas532001@outlook.com", "kd", "falpol2", "kunaldas532001@gmail.com")
# send_teacher_library_clearance_email_with_pdf("T018", "kunaldas532001@outlook.com", "kd", "falpol2", "kunaldas532001@gmail.com")
# send_library_email(cursor, studentid, book_id,  purpose, extra_info=None)

