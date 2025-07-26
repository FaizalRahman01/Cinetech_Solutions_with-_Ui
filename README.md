# Cinetech – Multiplex Management System

**Developed as a final-year capstone project**, *Cinetech* is a Flask-based web application that simulates a real-world multiplex environment. The system offers features like movie ticket booking, finance simulation, student performance management, sales analysis, and employee dashboards — all through a centralized and secure interface.

---

##  Features

### 1.  Movie Ticket Booking
- Select movie, showtime, and seat layout.
- Seat-based dynamic pricing.
- Automatic vehicle suggestion based on group size.
- Booking ID generation and summary dashboard.

### 2.  Finance Management Module
- Virtual ATM-like simulation.
- PIN-protected interface for secure transactions.
- Balance tracking, deposits, and withdrawals.

### 3.  Student Record System
- Add, search, and analyze student grades.
- Grade validation with average percentage calculation.
- Export records in Excel format.

### 4.  Employee Salary Dashboard
- View employee data sorted by salary.
- 10% salary hike preview without database modification.

### 5.  Sales Analysis
- Analyze dummy sales data with 10% tax calculation.
- Identify high-value transactions.
- Exportable Excel reports with categorized data.

### 6.  Admin Tools
- View all bookings from the database.
- One-click export of bookings, students, and sales reports (`.xlsx`).
- Flash messaging for user feedback and alerts.

---

##  Tech Stack

| Layer           | Tools Used                                |
|----------------|--------------------------------------------|
| **Frontend**    | HTML5, CSS3, Bootstrap 4, Jinja2 Templates |
| **Backend**     | Flask (Python)                             |
| **Database**    | SQLite3                                    |
| **Libraries**   | Pandas, random, datetime, flash            |

---
##  How to Run Cinetech-Solutions

Follow the steps below to run this Flask-based web application on your local machine.

---

###  Step 1: Clone the Repository

```bash
git clone https://github.com/FaizalRahman01/Cinetech_Solutions_with-_Ui
cd Cinetech_Solutions_with-_Ui
```
##  How to Run Cinetech-Solutions

Follow the steps below to run this Flask-based web application on your local machine.

---

### 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/FaizalRahman01/Cinetech_Solutions_with-_Ui
cd Cinetech_Solutions_with-_Ui
```

python -m venv venv
venv\Scripts\activate   # For Windows
# source venv/bin/activate  # For Linux/Mac
pip install -r requirements.txt  
pip freeze > requirements.txt  
python app.py  
Step 5: Open in Browser
Open your browser and visit:

👉 http://127.0.0.1:5000/
