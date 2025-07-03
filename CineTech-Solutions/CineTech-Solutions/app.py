from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pandas as pd
from types import SimpleNamespace
from database import create_connection
import random, datetime

app = Flask(__name__)
app.secret_key = 'R22CA1CA0067-Faizal_Rahman'

# Helper function to get database connection
def get_db_connection():
    conn = create_connection()
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    price = None
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            if age <= 0:
                flash('Invalid age. Please enter a positive number.', 'error')
            elif age <= 12:
                price = {'type': 'Child Ticket $', 'amount': 5}
            elif age <= 18 or age <= 21:
                price = {'type': 'Teenager Ticket $', 'amount': 8}
            elif age >= 22:
             price = {
                'type': 'Your ticket is not booked because you are above 21',
                 'amount': '\nYou are not eligible to book a ticket, please go to Movie Ticket Section',
                  'is_error': True    }
            print(price['type'])
            print(price['amount'])
            rice = {'type': 'Senior Citizen Ticket', 'amount': 7}
        except ValueError:
            flash('Invalid input. Please enter a valid number.', 'error')

    return render_template('ticket.html', price=price)

@app.route('/book', methods=['GET', 'POST'])
def book():
    vehicle = None
    vehicle_image = None
    total_price = 0  # New line: Initialize total price
    # Sample movie data - POST aur GET dono me use hoga, isliye yeh if block ke pehle hi hona chahiye
    movies = [
        {'name': 'Housefull 5', 'time': '11:00 AM - 02:00 PM', 'poster': url_for('static', filename='images/movie1.png')},
        {'name': 'Avatar The Way of Water', 'time': '2:30 PM - 06:30 PM', 'poster': url_for('static', filename='images/movie2.png')},
        {'name': 'Sitaare Zameen Par', 'time': '7:00 PM - 10:00 PM', 'poster': url_for('static', filename='images/movie3.png')}
    ]

    if request.method == 'POST':
        movie = request.form['movie']
        people = int(request.form['people'])
        payment = request.form['payment']
        seats = request.form['seats']  # e.g., "A5,B7"
        booking_id = random.randint(100000, 999999)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Vehicle logic as before
        if people == 1:
            vehicle = 'Bike1'
            vehicle_image = url_for('static', filename='images/bike1.png')
        elif  people == 2:
            vehicle = 'Bike'
            vehicle_image = url_for('static', filename='images/bike.png')
        elif people == 3:
            vehicle = 'Auto'
            vehicle_image = url_for('static', filename='images/auto.png')
        elif people == 4 or people == 5:
            vehicle = 'Taxi'
            vehicle_image = url_for('static', filename='images/taxi.png')
        elif people == 6 or people == 7:
            vehicle = 'scorpio'
            vehicle_image = url_for('static', filename='images/scorpio.png')
        else:
            vehicle = 'Bus'
            vehicle_image = url_for('static', filename='images/bus.png')

        # Calculate ticket price
        total_price = 0
        seat_list = seats.split(',')
        for seat in seat_list:
            seat_row = seat.strip()[0].upper()  # Get first character of seat, uppercase
            if seat_row == 'A':
                total_price += 230
            elif seat_row in ['B', 'C', 'D', 'E']:
                total_price += 260
            elif seat_row in ['F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
                total_price += 300
            else:
                total_price += 230  # fallback for unexpected rows

        # Store all details including price
        session['ticket_info'] = {
            'movie': movie,
            'people': people,
            'payment': payment,
            'seats': seats,
            'vehicle': vehicle,
            'price': total_price,         # ✅ add total price
            'booking_id': booking_id,     # ✅ Booking ID
            'timestamp': timestamp,       # ✅ Timestamp
            'poster': '',                 # ✅ Poster placeholder
            'time': ''                    # ✅ Show time placeholder
        }

        # ✅ Loop sirf POST ke andar chalega
        for m in movies:
            if m['name'] == movie:
                session['ticket_info']['poster'] = m['poster']
                session['ticket_info']['time'] = m['time']
                break

        return redirect(url_for('ticket_summary'))

    # GET request ke liye default vehicle image
    vehicle_image = None

    return render_template('book.html', movies=movies, vehicle_image=vehicle_image)


@app.route('/ticket_summary')
def ticket_summary():
    ticket_info = session.get('ticket_info')
    if not ticket_info:
        return redirect(url_for('book'))

    ticket_info = SimpleNamespace(**ticket_info)
    return render_template('ticket_summary.html', ticket_info=ticket_info)

@app.route('/finance', methods=['GET', 'POST'])
def finance():
    if request.method == 'POST':
        if 'pin' in request.form:
            try:
                entered_pin = int(request.form['pin'])
                conn = get_db_connection()
                finance_data = conn.execute('SELECT * FROM finance WHERE id = 1').fetchone()
                conn.close()

                if entered_pin == finance_data['pin']:
                    session['pin_verified'] = True
                    flash('PIN verified successfully!', 'success')
                else:
                    flash('Incorrect PIN. Please try again.', 'error')
            except ValueError:
                flash('Invalid PIN. Please enter numbers only.', 'error')

        elif 'amount' in request.form:
            if not session.get('pin_verified'):
                return redirect(url_for('finance'))

            try:
                amount = float(request.form['amount'])
                if amount <= 0:
                    flash('Amount must be positive.', 'error')
                    return redirect(url_for('finance'))

                conn = get_db_connection()
                finance_data = conn.execute('SELECT * FROM finance WHERE id = 1').fetchone()
                current_balance = finance_data['balance']

                if 'deposit' in request.form:
                    new_balance = current_balance + amount
                    conn.execute('UPDATE finance SET balance = ? WHERE id = 1', (new_balance,))
                    conn.commit()
                    flash(f'Deposit successful! New balance: ${new_balance:.2f}', 'success')
                elif 'withdraw' in request.form:
                    if amount > current_balance:
                        flash('Insufficient funds.', 'error')
                    else:
                        new_balance = current_balance - amount
                        conn.execute('UPDATE finance SET balance = ? WHERE id = 1', (new_balance,))
                        conn.commit()
                        flash(f'Withdrawal successful! New balance: ${new_balance:.2f}', 'success')

                conn.close()
            except ValueError:
                flash('Invalid amount.', 'error')

    conn = get_db_connection()
    finance_data = conn.execute('SELECT * FROM finance WHERE id = 1').fetchone()
    conn.close()

    return render_template('finance.html',
                           balance=finance_data['balance'],
                           pin_verified=session.get('pin_verified', False))

@app.route('/finance/logout')
def finance_logout():
    session.pop('pin_verified', None)
    flash('Logged out from finance portal.', 'info')
    return redirect(url_for('finance'))

@app.route('/student', methods=['GET', 'POST'])
def student():
    conn = get_db_connection()

    if request.method == 'POST':
        if 'add_student' in request.form:
            name = request.form['name'].strip()
            student_id = request.form['id']
            grades = request.form['grades']

            if not name.replace(' ', '').isalpha():
                flash('Invalid name. Only letters and spaces allowed.', 'error')
            else:
                try:
                    student_id = int(student_id)
                    if student_id <= 0:
                        flash('ID must be a positive number.', 'error')
                    else:
                        try:
                            grades_list = [int(g.strip()) for g in grades.split(',')]
                            if not all(0 <= g <= 100 for g in grades_list):
                                flash('Grades must be between 0-100.', 'error')
                            else:
                                existing = conn.execute('SELECT id FROM students WHERE id = ?', (student_id,)).fetchone()
                                if existing:
                                    flash('Student ID already exists.', 'error')
                                else:
                                    conn.execute('''
                                        INSERT INTO students (id, name, grades)
                                        VALUES (?, ?, ?)
                                    ''', (student_id, name, grades))
                                    conn.commit()
                                    avg_grade = sum(grades_list) / len(grades_list)
                                    flash(f'Student {name} added successfully with average grade {avg_grade:.2f}%', 'success')
                        except ValueError:
                            flash('Invalid grades. Must be numbers separated by commas.', 'error')
                except ValueError:
                    flash('Invalid ID. Must be a number.', 'error')

        elif 'search_id' in request.form:
            search_id = request.form['search_id']
            try:
                search_id = int(search_id)
                student = conn.execute('SELECT * FROM students WHERE id = ?', (search_id,)).fetchone()
                if student:
                    grades = [int(g) for g in student['grades'].split(',')]
                    avg = sum(grades) / len(grades)
                    session['search_result'] = {
                        'name': student['name'],
                        'id': student['id'],
                        'grades': student['grades'],
                        'average': avg
                    }
                else:
                    flash('Student ID not found', 'error')
            except ValueError:
                flash('Invalid ID. Must be a number.', 'error')

        elif 'threshold' in request.form:
            try:
                threshold = float(request.form['threshold'])
                if not 0 <= threshold <= 100:
                    flash('Threshold must be between 0-100', 'error')
                else:
                    students = conn.execute('SELECT * FROM students').fetchall()
                    above_threshold = []

                    for student in students:
                        grades = [int(g) for g in student['grades'].split(',')]
                        avg = sum(grades) / len(grades)
                        if avg > threshold:
                            above_threshold.append({
                                'name': student['name'],
                                'id': student['id'],
                                'average': avg
                            })

                    session['threshold_result'] = {
                        'threshold': threshold,
                        'students': above_threshold
                    }
            except ValueError:
                flash('Invalid threshold. Must be a number.', 'error')

    search_result = session.pop('search_result', None)
    threshold_result = session.pop('threshold_result', None)

    conn.close()
    return render_template('student.html', search_result=search_result, threshold_result=threshold_result)

@app.route('/employee')
def employee():
    conn = get_db_connection()

    employees = conn.execute('''
        SELECT * FROM employees 
        ORDER BY salary DESC
    ''').fetchall()

    updated_employees = []
    for emp in employees:
        updated_employees.append({
            'name': emp['name'],
            'salary': emp['salary'] * 1.10
        })

    conn.close()

    return render_template('employee.html', employees=employees, updated_employees=updated_employees)

@app.route('/sales')
def sales():
    sales_data = [200, 450, 700, 150, 900, 100, 220, 600, 450]
    tax_prices = [round(amount * 1.10, 2) for amount in sales_data]
    high_value = [amount for amount in sales_data if amount > 500]
    total_revenue = sum(tax_prices)

    return render_template('sales.html',
                           sales_data=sales_data,
                           tax_prices=tax_prices,
                           high_value=high_value,
                           total_revenue=total_revenue)

@app.route('/view_bookings')
def view_bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/export_bookings')
def export_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Movie', 'People', 'Payment', 'Seats', 'Vehicle'])
    file_path = 'static/exports/bookings.xlsx'
    df.to_excel(file_path, index=False)
    conn.close()
    return f'<a href="/{file_path}" download>Download Bookings Excel</a>'

@app.route('/export_students')
def export_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Grades'])
    file_path = 'static/exports/students.xlsx'
    df.to_excel(file_path, index=False)
    conn.close()
    return f'<a href="/{file_path}" download>Download Students Excel</a>'

@app.route('/export_sales')
def export_sales():
    sales_data = [200, 450, 700, 150, 900, 100, 220, 600, 450]
    tax_prices = [round(amount * 1.10, 2) for amount in sales_data]
    high_value = [amount for amount in sales_data if amount > 500]
    total_revenue = sum(tax_prices)

    df = pd.DataFrame({
        'Original Price': sales_data,
        'Price with Tax': tax_prices,
        'High Value': ['Yes' if amount > 500 else 'No' for amount in sales_data]
    })

    file_path = 'static/exports/sales.xlsx'
    df.to_excel(file_path, index=False)

    return f'<a href="/{file_path}" download>Download Sales Excel</a>'

if __name__ == '__main__':
    app.run(debug=True)
