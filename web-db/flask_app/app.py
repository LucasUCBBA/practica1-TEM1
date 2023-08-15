from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)
app.secret_key = "11223344"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/studentlist', methods=['GET'])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return render_template('list.html', students=data)

@app.route('/newStudent')
def add_student_form():
        return render_template('registerStudent.html')

@app.route('/add', methods=['POST'])
def add_student():
        conn = None
        cursor = None
        first_name = request.form['fName']
        last_name = request.form['lName']
        city = request.form['city']
        semester = request.form['semester']
        if first_name and last_name and city and semester and request.method == 'POST':
                sql = "INSERT INTO student(first_name, last_name, city, semester) VALUES(%s, %s, %s, %s)"
                data = (first_name, last_name, city, semester)
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect('/studentlist')
        else:
                return 'Error while adding user'

@app.route('/edit/<id>')
def get_student(id):
        conn = None
        cursor = None
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM student WHERE id = %s", id)
        data = cursor.fetchall()
        cursor.close()
        print(data[0])
        return render_template('editStudent.html', student=data[0])

@app.route('/update', methods=['POST'])
def update_student():
        conn = None
        cursor = None
        first_name  = request.form['fName']
        last_name = request.form['lName']
        city = request.form['city']
        semester = request.form['semester']
        id = request.form['id']
        if request.method == 'POST':
                sql = "UPDATE student set first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s"
                data = (first_name, last_name, city, semester, id)
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(sql,data)
                conn.commit()
                flash('Student Updated!')
                return redirect('/studentlist')

@app.route('/delete/<id>')
def delete_student(id):
        conn = None
        cursor = None
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id=%s", (id,))
        conn.commit()
        return redirect('/studentlist')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
