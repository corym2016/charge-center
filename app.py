# to open database: psql window -> enter -> 'chargercenter_db' -> enter -> enter -> 'Millecor98!'
# to run flask: cmd -> 'cd C:\Users\corym\Documents\Harvard Projects\charge-center' -> 'Envs\envChargeCenter\Scripts\activate' -> 'flask run'

import os, json

from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

import requests

# # MATLAB Optimizer and Variable Saving
# import matlab.engine
# engMATLAB = matlab.engine.start_matlab()

# imports for scheduling (APScheduler)
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon=True)
from datetime import datetime

app = Flask(__name__)

os.environ['FLASK_DEBUG'] = '1'
os.environ['DATABASE_URL'] = 'postgresql://postgres:Millecor98!@localhost:5433/chargecenter_db'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

# Initialize parameters
relay1_status = 'off'
relay2_status = 'off'
# requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'1','binary':'0'})
# requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'2','binary':'0'})

@app.route("/")
#@login_required
def index():
    session.clear()
    return render_template("home.html")
    # return render_template("chargerSearch.html")
    # return render_template("test.html")

@app.route("/Update", methods=["POST"])
def updateInfo():
    # Get form data
    plugStatus = request.form.get("plugStatus")
    miles = request.form.get("miles")
    alpha = request.form.get("alpha")
    # Update database
    db.execute("DELETE FROM chargers_log WHERE u_id = :user_id", {"user_id": session['user_id']})
    db.commit()
    db.execute("INSERT INTO chargers_log (u_id, charger_num, port_num, plug_status, miles, alpha) VALUES (:user_id, :charger_num, :port_num, :plugStatus, :miles, :alpha)", {"user_id":session['user_id'], "charger_num":session['charger_num'], "port_num":session['port_num'], "plugStatus":plugStatus, "miles":miles, "alpha":alpha})
    db.commit()

    # # USE WHEN YOU WANT TO INTEGRATE ACTUAL MATLAB - MUST UNCOMMENT MATLAB ENG
    # # Trigger Event - Optimization from MATLAB
    # dataIn = db.execute("SELECT * FROM chargers_log WHERE charger_num = :charger_num", {"charger_num": session['charger_num']}).fetchall()
    # print(dataIn)
    # # Send data to matlab function
    # dataOut = engMATLAB.testMATLAB(matlab.double(dataIn))
    # print(dataOut)

    # Update next page for current charger status
    ports = db.execute("SELECT port_num FROM chargers_log WHERE charger_num = :charger_num", {"charger_num": session['charger_num']}).fetchall()
    return render_template("chargerView.html", charger_num=session['charger_num'], port_num=session['port_num'])


@app.route("/Credentials", methods=["POST"])
def open():
    if request.form['creds'] == 'login':
        return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/RegistrationPage", methods=["POST"])
def open_register():
    return render_template("register.html")

@app.route("/Login", methods=["POST", "GET"])
def login():
    """Sign In Here."""
    # forget user data
    session.clear()
    # Get form username.
    username = request.form.get("username")
    # Check to make sure username exists
    user = db.execute("SELECT * FROM users WHERE u_username = :username", {"username": username}).fetchone()
    if user is None:
        return render_template("login.html", message="*Username does not exist.")
    else:
        if user == None or not check_password_hash(user[2], request.form.get("password")):
            return render_template("login.html", message="*Password incorrect.")
        else:
            # making the session variables - session.clear() when user logs out
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['charger_num'] = user[5]
            session['port_num'] = user[6]
            # grab that users review data
            # reviews = db.execute("SELECT * FROM reviews WHERE r_user_id = :user_id", {"user_id": session['user_id']}).fetchall()
            # length = len(reviews)
            # books = []
            # for review in reviews:
                # book_id = review['r_book_id']
                # book = db.execute("SELECT * FROM books WHERE b_id = :book_id", {"book_id": book_id}).fetchone()
                # books.append(book)
            # Sending users data to next page
            # return render_template("profile.html", user=user, books=books, reviews=reviews, length=length, message="Successfully signed in.")
            # return render_template("chargerSearch.html")
            # return render_template("relays_OFF.html")
            return render_template("formUpdateInfo.html")


@app.route("/UpdateInfo", methods=["GET","POST"])
def routeUpdateForm():
    return render_template("formUpdateInfo.html")

@app.route("/Register", methods=["GET", "POST"])
def register():
    """Register Here."""
    # clear session data
    session.clear()
    # Get form information.
    username = request.form.get("username")
    password = request.form.get("password")
    con_password = request.form.get("con_password")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    # Check to make sure username is not alread taken.
    usercheck = db.execute("SELECT * FROM users WHERE u_username = :username", {"username":username}).fetchone()
    if usercheck is None:
        if password == con_password:
            # Give them a Charger and Port number
            lastPort = db.execute("SELECT port_num FROM users ORDER BY u_id DESC LIMIT 1").fetchone()
            lastCharger = db.execute("SELECT charger_num FROM users ORDER BY u_id DESC LIMIT 1").fetchone()
            if not lastPort:
                port_num = 1
                charger_num = 1;
            elif lastPort[0] == 6:
                port_num = 1
                charger_num = lastCharger[0] + 1
            else:
                port_num = lastPort[0] + 1
                charger_num = lastCharger[0]
            # Hash password to store
            hashPass = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            # Add that users info to the database
            db.execute("INSERT INTO users (u_username, u_password, u_firstname, u_lastname, charger_num, port_num) VALUES (:username, :hashPass, :firstname, :lastname, :charger_num, :port_num)", {"username":username, "hashPass":hashPass, "firstname":firstname, "lastname":lastname, "charger_num":charger_num, "port_num":port_num})
            db.commit()
            return render_template("login.html", message="Succesfully registered, please sign in.")
        else:
            return render_template("register.html", message="*Passwords do not match. Please try again.")
    else:
        return render_template("register.html", message="*Username already taken, please choose a different username.")


# @app.route("/relay1_toggle", methods=["POST"])
# def relay1_toggle():
#     global relay1_status
#     relay1_status = request.form['relay1_switch']
#     if relay1_status == 'on':
#         requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'1','binary':'1'})
#         if relay2_status == 'on':
#             return render_template("relays_ON.html")
#         else:
#             return render_template("relay1_ON.html")
#     else:
#         requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'1','binary':'0'})
#         if relay2_status == 'on':
#             return render_template("relay2_ON.html")
#         else:
#             return render_template("relays_OFF.html")
#
# @app.route("/relay2_toggle", methods=["POST"])
# def relay2_toggle():
#     global relay2_status
#     relay2_status = request.form['relay2_switch']
#     if relay2_status == 'on':
#         requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'2','binary':'1'})
#         if relay1_status == 'on':
#             return render_template("relays_ON.html")
#         else:
#             return render_template("relay2_ON.html")
#     else:
#         requests.post('http://192.168.1.33/setRelay', json = {'relayNum':'2','binary':'0'})
#         if relay1_status == 'on':
#             return render_template("relay1_ON.html")
#         else:
#             return render_template("relays_OFF.html")
#
# @app.route("/ChargeSchedule", methods=["GET", "POST"])
# def chargerSearch():
#     chargerNum = request.form['chargerNum']
#     # chargerPort = request.form['chargerPort']
#     numPorts = db.execute("SELECT ch_ports FROM chargers WHERE ch_num = :chargerNum", {"chargerNum":chargerNum}).fetchone()
#     proxy = []
#     proxy_num = []
#     for i in range(1,numPorts[0]+1):
#         getProxy_url = 'http://192.168.1.33/getProxy'
#         # add value to proxy list (proxy is list of on or off for each proxy signal)
#         proxy.append(int(requests.get(getProxy_url).json()['proxy'+str(i)]))
#         proxy_num.append(i)
#     # get charger data (who is charging at what times) and pass to html
#     charger_data = db.execute("SELECT * FROM charger"+chargerNum).fetchall()
#     # get current time during request (start time)
#     hr_notMilt = datetime.now().strftime("%I")
#     am_pm = datetime.now().strftime("%p")
#     min = datetime.now().strftime("%M")
#     # check if any cars are plugged in. if not pass warning message
#     if all(p == 0 for p in proxy):
#         message = "Ensure that vehicle is plugged in..."
#         return render_template("chargerView.html", chargerNum=chargerNum, numPorts=numPorts, charger_data=charger_data, proxy=proxy, proxy_num=proxy_num, hr_notMilt=hr_notMilt, am_pm=am_pm, min=min, message=message)
#     else:
#         return render_template("chargerView.html", chargerNum=chargerNum, numPorts=numPorts, charger_data=charger_data, proxy=proxy, proxy_num=proxy_num, hr_notMilt=hr_notMilt, am_pm=am_pm, min=min)
#
# # Method to add schedule a time for a charger (add yourself to the line)
# @app.route("/ChargeSchedule/Charger<chargerNum>", methods=["GET"])
# def portRequest(chargerNum):
#     # Get user input arguments
#     port_req = int(request.args.get("port_select"))
#     chargerPort = port_req
#     # check to see if there are any current chargers before this request
#     charger_data = db.execute("SELECT * FROM charger"+chargerNum).fetchall()
#     return render_template("scheduler.html", chargerNum=chargerNum, chargerPort=chargerPort, charger_data=charger_data)
#
# # Method to add schedule a time for a charger (add yourself to the line)
# @app.route("/ChargeSchedule/Charger<chargerNum>/Port<chargerPort>", methods=["GET"])
# def chargeRequest(chargerNum,chargerPort):
#     # Load necessary data
#     charger_data = db.execute("SELECT * FROM charger"+chargerNum).fetchall()
#     # first check if port token correct
#     portToken =request.args.get("portToken")
#     if portToken == "pass":
#         # Get user input arguments
#         time_req = int(request.args.get("time_req"))
#         end_time = int(request.args.get("done_time"))
#         # get current time during request (start time)
#         hr = int(datetime.now().strftime("%H"))
#         min = int(datetime.now().strftime("%M"))
#         start_time = (hr*60) + min
#         end_time = end_time + start_time
#         # if first in line (no one else before charging) then immediately start charging, turn on relay1
#         if len(charger_data) == 0:
#             requests.post('http://192.168.1.33/setRelay', json = {'relayNum':chargerPort,'binary':'1','chargeDur':time_req})
#         # add data to database Table for specifiic charger to track its line
#         db.execute("INSERT INTO charger"+chargerNum+"(port_req, time_req, start_time, end_time) VALUES\
#                     (:port_req_in, :time_req_in, :start_time_in, :end_time_in)",
#                     {"port_req_in": chargerPort,
#                     "time_req_in": time_req,
#                     "start_time_in": start_time,
#                     "end_time_in": end_time})
#         db.commit()
#         # reload charger data for html page
#         charger_data = db.execute("SELECT * FROM charger"+chargerNum).fetchall()
#         # pull up charger schedule page again with updates
#         return render_template("scheduler.html", chargerNum=chargerNum, chargerPort=chargerPort, charger_data=charger_data)
#     if portToken != "pass":
#         message = "Incorrect Port Token..."
#         return render_template("scheduler.html", chargerNum=chargerNum, chargerPort=chargerPort, charger_data=charger_data, message=message)

# app.run(host='0.0.0.0')
