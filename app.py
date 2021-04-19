from flask import Flask, request, redirect, flash
from flask import render_template
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"

STAV_KEY = '123'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
   password="",
   database="webdemo"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Prayers (point VARCHAR(255), tag VARCHAR(255))")

@app.route('/prayer_show')
def prayer_show():
    mycursor.execute("SELECT * FROM Prayers")
    myresult = mycursor.fetchall()

    return render_template('prayer_show.html', myresult=myresult)

@app.route('/')
def main():
    return render_template('index.html')
#  
@app.route('/auth_page', methods=['GET', 'POST'])
def auth_page():
    error = None
    if request.method == "POST" : 
            key = request.form['key']

            if key == STAV_KEY :
                # who = 'stavin'
                flash('You were successfully logged in') 
                return redirect('/prayer_show')
        
            else:
                flash('Incorrect password')

    return render_template('auth.html')




@app.route('/input', methods=['GET', 'POST'])
def inputs():
    if request.method=='POST':
        point = request.form['point']
        tag = request.form['tag']
        sql = "INSERT INTO Prayers (point, tag) VALUES (%s, %s)"
        val = (point, tag)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect("/")
    return render_template('input.html')




if __name__ == '__main__':
   app.run(debug=True)