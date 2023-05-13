from flask import Flask, render_template, request,url_for, flash, redirect,session
import sqlite3
import sendgrid
import os
import re
from sendgrid.helpers.mail import *

app = Flask(__name__)

app.secret_key="1"

con = sqlite3.connect("pda.db")
#signin
con.execute("""CREATE TABLE IF NOT EXISTS 
signin1(pid INTEGER primary key, 
username TEXT, 
usermail TEXT, 
usercontact INTEGER, 
password TEXT)
""")

#donor
con.execute("""CREATE TABLE IF NOT EXISTS 
donor1(pid INTEGER primary key, 
name TEXT, 
mobile INTEGER, 
email TEXT, 
age INTEGER, 
gender TEXT,
blood TEXT, 
city TEXT, 
district TEXT)""")

#request
con.execute("""CREATE TABLE IF NOT EXISTS
request(pid INTEGER primary key,
drmail TEXT,
hospitalname TEXT,
recname TEXT,
recmobile INTEGER,
recmail TEXT,
recage INTEGER,
recgender TEXT,
recbloodgroup TEXT,
recarea TEXT,
reccity TEXT,
recdistrict TEXT)""")
con.close()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/login",methods = ['POST', 'GET'])
def login():
    msg = ''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=sqlite3.connect("pda.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from signin1 where username=? and password=?",(username,password))
        data=cur.fetchone()

        if data:
            session['username']=data['username']
            session['password']=data['password']
            msg = 'Logged In Successfully!'
            return redirect(url_for('afterlogin'))
        else:
            msg = 'Incorrect Username/Password!'
    return render_template('login.html', msg = msg)

@app.route("/signin",methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        usermail = request.form['usermail']
        usercontact = request.form['usercontact']
        password = request.form['password']
        con=sqlite3.connect("pda.db")
        cur=con.cursor()
        data=cur.fetchone()

        if (data):
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', usermail):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            # mailtest_registration(usermail)
            cur.execute("""INSERT 
            INTO signin1(username, usermail, usercontact, password)
            values(?,?,?,?)""",(username, usermail, usercontact, password))
            con.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('signin.html')


@app.route('/afterlogin')
def afterlogin():
    return render_template("user_profile.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

#----------------------------------------------------------------------------------------------------------------------

def mailtest_registration(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= 'apikey' )
    from_email = Email("chinnukool72@gmail.com")
    subject = "Registration Successfull!"
    content = Content("text/plain", "You have successfully registered as user. Please Login using your Username and Password to donate/request for Plasma.")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
#for donor
def mailtest_donor(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= 'apikey' )
    from_email = Email("chinnukool72@gmail.com")
    subject = "Thankyou for Registering as Donor!"
    content = Content("text/plain", "Every donor is an asset to the nation who saves people's lives, and you're one of them.We appreciate your efforts. Thank you!!")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
#for request
def mailtest_request(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= 'apikey' )
    from_email = Email("chinnukool72@gmail.com")
    subject = "Request Submitted!"
    content = Content("text/plain", "Your request has been successfully submitted. Please be patient, your requested donor will get back to you soon.")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
#for request sending to donor
def mailtest_requesttodonor(to_email):
    sg = sendgrid.SendGridAPIClient(api_key= 'apikey' )
    from_email = Email("chinnukool72@gmail.com")
    subject = "Requesting Plasma"
    content = Content("text/plain", "Your registration has been requested by a recipient, we will share futher details in future. Stay connected!!")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


#----------------------------------------------------------------------------------------------------------------------


@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/adddonor", methods = ['POST','GET'])
def adddonor():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        blood = request.form['blood']
        city = request.form['city']
        district = request.form['district']
        con = sqlite3.connect("pda.db")
        cur = con.cursor()
        data = cur.fetchone()

        if data:
            return render_template('donor.html', msg="You are already a member, please login using your details")

        else:
            # mailtest_donor(email)
            cur.execute("""INSERT 
            INTO donor1(name, mobile, email, age, gender, blood, city, district)
            values(?,?,?,?,?,?,?,?)""",(name, mobile, email, age, gender, blood, city, district))
            con.commit()

        return render_template('success.html', msg="Registered successfuly..")


@app.route("/donorlist")
def donorlist():
    con = sqlite3.connect("pda.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT email, age, gender, blood, city, district FROM donor1")
    donor1 = cur.fetchall()
    con.close()
    return render_template('donor.html', donor1 = donor1)

#----------------------------------------------------------------------------------------------------------------

@app.route("/request_page", methods = ['GET','POST'])
def request_page():
    msg = ''
    if request.method == 'POST' :
        drmail = request.form['drmail']
        hospitalname = request.form['hospitalname']
        recname = request.form['recname']
        recmobile = request.form['recmobile']
        recmail = request.form['recmail']
        recage = request.form['recage']
        recgender = request.form['recgender']
        recbloodgroup = request.form['recbloodgroup']
        recarea = request.form['recarea']
        reccity = request.form['reccity']
        recdistrict = request.form['recdistrict']
        con=sqlite3.connect("pda.db")
        cur=con.cursor()
        data=cur.fetchone()
        
        if data:
            msg = 'Request already exists !'
        else:
            # mailtest_request(recmail)
            # mailtest_requesttodonor(drmail)
            cur.execute("""INSERT 
            INTO request(drmail, hospitalname, recname, recmobile, recmail, recage, recgender, recbloodgroup, recarea, reccity, recdistrict)
            values(?,?,?,?,?,?,?,?,?, ?, ?)""",(drmail, hospitalname, recname, recmobile, recmail, recage, recgender, recbloodgroup, recarea, reccity, recdistrict))
            con.commit()
            msg = 'Your request has been submitted!'
            return render_template('request.html', msg = msg)

    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('request.html', msg = msg)

#-----------------------------------------------------------------------------------------------------------

@app.route('/dashboard',methods=['GET'])
def dashboard():
 if request.method == "GET":
     with sqlite3.connect("pda.db") as con:
             con.row_factory = sqlite3.Row  
             cur = con.cursor()
             m = con.cursor()
             cur.execute("SELECT * from donor1")
             rows = cur.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='O+'") #Total O+
             Opositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='O-'") #Total O-
             Onegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='A+'") #Total A+
             Apositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='A-'") #Total A-
             Anegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='B+'") #Total B+
             Bpositive = m.fetchall() 
             m.execute("SELECT COUNT(*) FROM donor1 where blood='B-'") #Total B-
             Bnegative = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='AB+'") #Total AB+
             ABpositive = m.fetchall()
             m.execute("SELECT COUNT(*) FROM donor1 where blood='AB-'") #Total AB-
             ABnegative = m.fetchall()
             m.execute("SELECT COUNT(name) FROM donor1") #Total no.of donors
             row = m.fetchall()

             return render_template('dashboard.html',Opositive = Opositive, Onegative = Onegative, Apositive = Apositive, Anegative = Anegative,Bpositive = Bpositive, Bnegative = Bnegative,ABpositive = ABpositive , ABnegative = ABnegative, rows = rows, row = row)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)