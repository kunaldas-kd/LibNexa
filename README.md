# 🌌 LibNexa: The Ultimate Library Management Ecosystem

![LibNexa Banner](https://img.shields.io/badge/LibNexa-Next--Gen--LMS-blue?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-1.2.0--stable-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20|%20MySQL%20|%20Webview-blueviolet?style=flat-square)

---

## 📖 Table of Contents

1.  [Introduction](#introduction)
    *   [Mission Statement](#mission-statement)
    *   [Target Audience](#target-audience)
2.  [Core Feature Matrix](#core-feature-matrix)
    *   [Administrative Control](#administrative-control)
    *   [Student & Teacher Management](#student--teacher-management)
    *   [Library Inventory Control](#library-inventory-control)
    *   [Financial & Fine Tracking](#financial--fine-tracking)
    *   [Communication & Notifications](#communication--notifications)
3.  [Technology Stack](#technology-stack)
    *   [Backend (Python)](#backend-python)
    *   [GUI Wrapper (PyWebView)](#gui-wrapper-pywebview)
    *   [Database (MySQL)](#database-mysql)
    *   [Frontend (HTML5/CSS3/JS)](#frontend-html5css3js)
4.  [High-Level Architecture](#high-level-architecture)
    *   [System Flow Diagrams](#system-flow-diagrams)
    *   [Logical Separation](#logical-separation)
5.  [Directory Structure](#directory-structure)
6.  [Prerequisites & Environment Setup](#prerequisites--environment-setup)
    *   [System Requirements](#system-requirements)
    *   [Python Installation](#python-installation)
    *   [MySQL Configuration](#mysql-configuration)
7.  [Installation Guide](#installation-guide)
    *   [Cloning the Repository](#cloning-the-repository)
    *   [Installing Dependencies](#installing-dependencies)
    *   [Initial Database Setup](#initial-database-setup)
8.  [Database Schema Documentation](#database-schema-documentation)
    *   [`Users` Table](#users-table)
    *   [`Book_Stock` Table](#book_stock-table)
    *   [`Books` Table](#books-table)
    *   [`Students` Table](#students-table)
    *   [`Borrowed_Books` Table](#borrowed_books-table)
    *   [`Cash_Book` Table](#cash_book-table)
    *   [`Teachers` Table](#teachers-table)
    *   [`Admin_Interface` Setup](#admin_interface-setup)
9.  [Logic Module Deep-Dive (Logics/ Directory)](#logic-module-deep-dive-logics-directory)
    *   [`database_setup.py`](#database_setuppy)
    *   [`send_email.py`](#send_emailpy)
    *   [`DOWNLOAD_section.py`](#download_sectionpy)
    *   [`transaction.py`](#transactionpy)
    *   [`EXCEL_DATA_PROCESSOR.py`](#excel_data_processorpy)
    *   [`Library_clearence.py`](#library_clearencepy)
10. [Frontend Template Documentation](#frontend-template-documentation)
    *   [Main Interface](#main-interface)
    *   [Dashboard & Analytics](#dashboard--analytics)
    *   [List Views & Search](#list-views--search)
11. [JS-Python Bridge (API Reference)](#js-python-bridge-api-reference)
12. [Security & Reliability](#security--reliability)
    *   [MAC Address Verification](#mac-address-verification)
    *   [OTP Authentication](#otp-authentication)
    *   [Data Backup & Recovery](#data-backup--recovery)
13. [Operational User Manual](#operational-user-manual)
    *   [Librarian Workflow](#librarian-workflow)
    *   [Student Workflow](#student-workflow)
14. [Troubleshooting & FAQ](#troubleshooting--faq)
15. [Deployment & Maintenance](#deployment--maintenance)
16. [Roadmap & Future Enhancements](#roadmap--future-enhancements)
17. [Contributing & Code of Conduct](#contributing--code-of-conduct)
18. [License & Acknowledgments](#license--acknowledgments)

---

## 1. Introduction

### Welcome to LibNexa
**LibNexa** is a sophisticated, desktop-based Library Management System (LMS) designed to revolutionize how educational institutions handle their physical and digital assets. By blending the robustness of a Python-based backend with the elegance of modern web technologies via PyWebView, LibNexa provides a fast, responsive, and cross-platform experience.

### Mission Statement
Our mission is to provide an all-in-one solution that reduces the administrative overhead of library management. LibNexa isn't just about tracking books; it's about building a digital bridge between librarians, teachers, and students through automated notifications, precise financial tracking, and comprehensive reporting.

### Target Audience
*   **School & College Libraries**: Tailored for institutions needing multi-tenant student/teacher tracking.
*   **Public Libraries**: Ideal for community centers requiring local database management without high internet reliance.
*   **Corporate Information Centers**: Suitable for managing internal documentation and asset borrowing.

---

## 2. Core Feature Matrix

| Category | Feature | Description |
| :--- | :--- | :--- |
| **User Management** | Student Registration | Full profile management including admission year and department tracking. |
| | Teacher Onboarding | Specific workflows for faculty members with different borrowing privileges. |
| | Passed-out Records | Dedicated table for alumni with certificate generation capabilities. |
| **Inventory** | Stock Management | Bulk book entry via Excel, tracking by publisher, edition, and source. |
| | Individual Book Tracking | Unique IDs for every copy to track precise borrow/return history. |
| | Missing Book Recovery | Logic to track lost items and charge appropriate recovery fees. |
| **Transactions** | Issue/Return System | Real-time status updates and automated due date calculation. |
| | Renewal Automation | Easy one-click renewals with balance check integration. |
| | Library Clearance | Automated clearance certificates for graduating students. |
| **Finance** | Cashbook Tracking | Integrated ledger for credit/debit transactions (fines, payments). |
| | Fine Calculation | Dynamic penalty calculation based on institutional rules. |
| | Fund Management | Tracking of library funds and miscellaneous expenditures. |
| **Communication** | Email Notifications | Automated OTPs, credential delivery, and due-date reminders. |
| | Report Export | Generate professional Excel and PDF reports for all data tables. |
| **Security** | MAC Authentication | Device-level locking to prevent unauthorized access. |
| | Auto Backup | Local database backup and recovery tools to ensure data safety. |

---

## 3. Technology Stack

LibNexa leverages a carefully curated stack to balance performance, aesthetics, and ease of deployment.

### Backend (Python 3.10+)
*   **Logic Core**: Modular Python code organized into specialized "Logics" packages.
*   **Threading**: Async background processing for emails and heavy data imports to keep the UI fluid.
*   **Email Engine**: `smtplib` and `MIME` libraries for high-deliverability notifications.
*   **Data Analysis**: `Pandas` and `OpenPyXL` for complex report generation and Excel processing.

### GUI Wrapper (PyWebView)
*   **Bridge**: Utilizing `pywebview`'s JS-Python bridge to expose backend methods to the frontend.
*   **Engine**: EdgeChromium (on Windows) or WebKit (on Linux/Mac) for rendering high-fidelity HTML templates as a standalone app.

### Database (MySQL 8.0)
*   **Structure**: Multi-tenant architecture allowing each institution to have its own isolated database schema.
*   **Connectivity**: `mysql-connector-python` for high-performance CRUD operations.

### Frontend (HTML5/CSS3/JS)
*   **Styling**: Premium CSS layouts (vanilla) with a focus on dark mode and responsive grids.
*   **Interactivity**: Vanilla JavaScript for handling UI state and calling exposed Python APIs.

---

## 4. High-Level Architecture

LibNexa follows a "Headless-Hybrid" architecture where the application logic exists completely independently of the presentation layer.

### System Flow
1.  **Entry Point**: `Main.py` initializes the splash screen and establishes the MySQL connection.
2.  **Interface Loading**: PyWebView loads the requested HTML template (e.g., `dashboard.html`).
3.  **User Action**: A user clicks a button, triggering a JS function.
4.  **Bridge Execution**: The JS function calls `window.pywebview.api.some_method()`.
5.  **Logic Processing**: The corresponding Python method in `Logics/` executes DB queries or system commands.
6.  **Callback**: Python returns data (usually as a JSON object) which JS then renders in the UI.

### Logical Separation
*   **Templates**: Pure presentation Layer.
*   **APIs**: Mediation Layer (converts web calls to logic calls).
*   **Logics**: Domain Layer (business rules, db setup).

---

## 5. Directory Structure

```plaintext
LibNexa/
├── Logics/                 # Core Business Logic
│   ├── database_setup.py   # DB Initialization & Schema
│   ├── send_email.py       # SMTP Automation
│   ├── DOWNLOAD_section.py # Report Generation
│   ├── transaction.py      # Issue/Return Logic
│   ├── ... (40+ modules)
├── templates/              # HTML/CSS/JS Assets
│   ├── dashboard.html      # Main Control Panel
│   ├── student_list.html   # User Management UI
│   ├── ... (25+ screens)
├── IMG/                    # Image Assets
├── Main.py                 # Application Entry Point
├── backup.py               # Database Maintenance Tool
├── LICENSE                 # MIT License
└── README.md               # You Are Here
```

---

## 6. Prerequisites & Environment Setup

### System Requirements
*   **OS**: Windows 10/11 (Preferred), Linux (Ubuntu 20.04+), macOS.
*   **RAM**: 4GB Minimum (8GB Recommended).
*   **Storage**: 100MB for App + Space for Database & Backups.
*   **Drivers**: WebView2 Runtime (For Windows/Edge support).

### Python Installation
1.  Download Python 3.10+ from [python.org](https://www.python.org/).
2.  Enable "Add Python to PATH" during installation.
3.  Verify: `python --version`

### MySQL Configuration
1.  Install MySQL Server 8.0+.
2.  Set a strong root password.
3.  Create an admin user or ensure root has `ALL PRIVILEGES`.
4.  Note down the Host, Port, User, and Password for `database_connector.py`.

---

## 7. Installation Guide

### Step 1: Clone the Repo
```bash
git clone https://github.com/your-username/LibNexa.git
cd LibNexa
```

### Step 2: Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Step 3: Install Core Dependencies
```bash
pip install pywebview mysql-connector-python pandas openpyxl matplotlib jinja2
```

### Step 4: Configure Database Connector
Open `Logics/database_connector.py` and update your credentials:
```python
def connect_to_db(db_name=None):
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database=db_name
    )
```

### Step 5: Launch
```bash
python Main.py
```

---

## 8. Database Schema Documentation

LibNexa uses a specialized schema designed for scalability and high-concurrency library operations.

### `Users` Table
*Primary table for institutional branding and system-wide settings.*
*   `Id`: Unique Institution ID.
*   `Library_name`: Display name of the library.
*   `Institute_Email`: Primary contact for automated emails.
*   `Late Fine Amount`: Daily penalty rate.
*   `Borrowing Period`: Default duration (in days) a book can be held.
*   `Payment Functionality`: Toggle (0 / 1) to enable/disable fine tracking.

### `Book_Stock` Table
*Tracks the master inventory and acquisition history.*
*   `Book_Name`, `Author`, `Edition`, `Publisher`: Core metadata.
*   `QTY`: Current total quantity in stock.
*   `Order_Challan_Bill_Info`: Audit trail for purchases.
*   `Is_BookID_Assigned`: (Yes/No) tracker for labeling.

### `Books` Table
*Granular tracking for every physical copy.*
*   `Book_ID`: Unique barcode/asset tag.
*   `Stock_Status`: (In Stock / Out of Stock / Damaged / Missing).

### `Students` Table
*Detailed student repository.*
*   `Student_ID`: Unique ID for borrowing.
*   `Admission_Year`: Tracks graduation timeline for clearance.
*   `Department`: Used for department-specific reporting.

### `Borrowed_Books` Table
*The core transactional ledger.*
*   `Borrow_Date`, `Return_Date`: Planned dates.
*   `Payable_Amount`: Calculation field for fines.
*   `Borrow`, `Submit`, `Renew`: Boolean flags for item status.
*   `Reminder`: Tracks if a due-date email has been sent.

### `Cash_Book` Table
*Financial audit trail.*
*   `Transaction_Id`: GUID for the payment.
*   `Debit` / `Credit`: Tracking fine income vs expenses.
*   `Balance`: Real-time account balance after every transaction.

---

## 9. Logic Module Deep-Dive

### `database_setup.py`
This module is responsible for initializing the multi-tenant environment. When a new institution registers, this module creates a dedicated `ID_library_db` and runs the SQL scripts to build the tables described in Section 8. It also handles the `Admin_Interface` initialization.

### `send_email.py`
The heartbeat of the communication system. It contains specialized functions:
*   `send_email(...)`: Dispatches welcome credentials via HTML-formatted emails.
*   `send_reminder_email_1(...)`: Friendly reminder 3 days before due date.
*   `send_reminder_email_2(...)`: Urgent penalty notification after deadline missed.
*   `send_otp_email(...)`: Generates and sends a 6-digit verification code.
*   `send_library_clearance_email_with_pdf(...)`: Attaches a generated PDF certificate and mails it to graduating students.

### `DOWNLOAD_section.py`
A heavy-duty reporting module. It uses `Pandas` to fetch database records and export them as professional Excel files.
*   **Smart Filtering**: Allows users to export books by "Publisher AND Year" or Students by "Department AND Admission Year".
*   **Sanitization**: Automatically handles invalid characters in filenames.
*   **Version Control**: If a file is open in Excel, it automatically creates a new version (e.g., `Report_1.xlsx`) instead of crashing.

### `transaction.py`
Handles the transition states of books.
*   **Submit Logic**: Checks if a book is overdue, calculates the fine via `total_amount_taking.py`, updates the `borrowed_books` record, increments stock levels, and sends a confirmation email.
*   **Renewal Logic**: Extends the return date by fetching the `Borrowing Period` from the user's settings. It blocks renewals if there are pending fines above a certain threshold (if enabled).

---

## 10. Frontend Template Documentation

LibNexa features a modern, intuitive UI designed for ease of use in fast-paced environments.

### `main.html` & `splash.html`
The initialization sequence. `splash.html` provides a branded entry experience while `Main.py` checks system integrity, internet status (via `CHECK_INTERNET.py`), and database availability before loading the login screen.

### `dashboard.html`
The central hub. It features a "Quick Stats" bar showing:
*   Total Books in Stock
*   Active Borrows
*   Today's Pending Submissions
*   Total Fines Collected
*   Active Students/Teachers

### `Setting.html`
An administrative powerhouse. Librarians can:
*   Update individual student/teacher passwords.
*   Change the institution's contact details and logo.
*   Adjust fine rates and borrowing periods in real-time without needing a restart.
*   Toggle system functionalities like "Payment Tracking".

---

## 11. JS-Python Bridge (API Reference)

For developers looking to extend LibNexa, the core APIs are exposed through the `webview` bridge.

### Authentication API
`Login_API.py` exposess methods to the `login.html` interface:
```javascript
// JS call
window.pywebview.api.login(username, password).then(response => {
    if(response.auth) { window.location = "dashboard.html"; }
});
```

### Student Management API
`Student_entry_API.py` methods:
*   `register_student(data)`: Validates and inserts a new student record.
*   `view_student(id)`: Fetches full profile and borrow history.

---

## 12. Security & Reliability

### MAC Address Verification
To ensure data security, LibNexa can be locked to a specific administrator device. The system captures the machine's MAC address during the first login and stores it. Future attempts from different hardware will trigger an "Unauthorized Device" alert.

### OTP Authentication
Password recovery and high-sensitivity actions (like purging records) are protected by a two-factor authentication (2FA) layer via Email OTP.

### Data Backup & Recovery
The `backup.py` utility can be scheduled to run every 24 hours. It performs a `mysqldump` of the institution's database and saves it as a timestamped `.sql` file in the `IMG/` or a dedicated backup directory. Recovery is as simple as running the `restore` command through the admin interface.

---

## 13. Operational User Manual

### Librarian Workflow: Issuing a Book
1.  Open **Dashboard** -> Click **Issue Book**.
2.  Input **Student ID** (System auto-checks for existing fines).
3.  Input **Book ID** (System verifies 'In Stock' status).
4.  Confirm Issue -> Student receives **Confirmation Email** instantly.

### Librarian Workflow: Missing Book Recovery
1.  Navigate to **Missing Book Register**.
2.  Search for the Book ID.
3.  Assess recovery cost (Auto-calculated based on book price + processing fee).
4.  Process recovery -> System moves status to 'Recovered' or 'Lost' and updates the Cashbook.

---

## 14. Troubleshooting & FAQ

**Q: Application fails to start after splashing.**
*   Check if MySQL Server is running.
*   Ensure the database credentials in `Logics/database_connector.py` match your setup.

**Q: Emails are not being sent.**
*   LibNexa uses Gmail's SMTP by default. Ensure "Less Secure Apps" is on or use an **App Password**.
*   Check your internet connection via the dashboard status indicator.

**Q: Excel exports fail.**
*   Ensure you have write permissions to your 'Downloads' folder.
*   Make sure the file you are trying to overwrite isn't currently open in another program.

---

## 16. Roadmap & Future Enhancements

*   [ ] **Mobile Companion App**: A React Native app for students to check their due dates.
*   [ ] **AI Recommendation Engine**: Suggest books based on a student's past borrow history.
*   [ ] **Barcode Scanner Integration**: Faster issue/return via USB barcode scanners.
*   [ ] **Cloud Sync**: Optional PostgreSQL support for cloud deployments.

---

## 17. Contributing & Code of Conduct

We welcome contributions from the community!
1.  Fork the repository.
2.  Create your feature branch: `git checkout -b feature/AmazingFeature`.
3.  Commit your changes: `git commit -m 'Add some AmazingFeature'`.
4.  Push to the branch: `git push origin feature/AmazingFeature`.
5.  Open a Pull Request.

---

## 18. License & Acknowledgments

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

### Special Thanks
*   **Nestive Tech Team**: For the core logic development.
*   **PyWebView Community**: For the incredible bridge framework.
*   **Open Source Maintainers**: To all libraries used (Pandas, OpenPyXL, etc.).

---
**LibNexa - Empowering Knowledge, Digitally.**
Documentation Version: 1.0.0 | Last Updated: 2026-03-31
