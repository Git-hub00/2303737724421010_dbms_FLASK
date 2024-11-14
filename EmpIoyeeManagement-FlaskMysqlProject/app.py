from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'gowtham'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2005'
app.config['MYSQL_DB'] = 'hospital'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patientdetails")
    patientinfo = cur.fetchall()
    cur.close()
    return render_template('patients.html', patients=patientinfo)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    search_term = ''
    if request.method == "POST":
        search_term = request.form['patientid']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM patientdetails WHERE id LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)
        cur.close()
        return render_template('patients.html', patients=search_results)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        iddata = request.form['patientid']
        name = request.form['name']
        description = request.form['description']
        disease = request.form['disease']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patientdetails (id, name, discription, disease) VALUES (%s, %s, %s, %s)", (iddata, name, description, disease))
        mysql.connection.commit()
        return redirect(url_for('patients'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patientdetails WHERE id = %s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('patients'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['patientid']
        name = request.form['name']
        description = request.form['description']
        disease = request.form['disease']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE patientdetails SET name = %s, discription = %s, disease = %s WHERE id = %s", (name, description, disease, id_data))
        mysql.connection.commit()
        return redirect(url_for('patients'))

if __name__ == "__main__":
    app.run(debug=True)
