from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'nakul'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2005'
app.config['MYSQL_DB'] = 'hospital_db'
mysql = MySQL(app)

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    search_query = request.form.get('search') if request.method == 'POST' else ''
    
    if search_query:
        cur.execute("SELECT * FROM patients WHERE name LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM patients")
    
    patients = cur.fetchall()
    cur.close()
    
    return render_template('dashboard.html', patients=patients, search_query=search_query)

@app.route('/patient/new', methods=['GET', 'POST'])
def create_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']
        contact = request.form['contact']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (name, age, condition, contact) VALUES (%s, %s, %s, %s)", (name, age, condition, contact))
        mysql.connection.commit()
        cur.close()
        flash('Patient record added successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('patient_form.html')

@app.route('/patient/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE id = %s", [id])
    patient = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']
        contact = request.form['contact']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (name, age, patient_condition, contact) VALUES (%s, %s, %s, %s)", (name, age, patient_condition, contact))
        mysql.connection.commit()
        cur.close()
        flash('Patient record updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('patient_form.html', patient=patient)

@app.route('/patient/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patients WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Patient record deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
    