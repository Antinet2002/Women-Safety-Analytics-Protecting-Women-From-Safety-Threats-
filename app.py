import os
print("TEMPLATE FOLDER:", os.path.join(os.getcwd(), "templates"))
from flask import Flask, render_template, request, jsonify
import sqlite3
from alerts import send_alert

app = Flask(__name__)

# DB Setup
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        threat TEXT,
        latitude TEXT,
        longitude TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')

# Save incident + trigger alert
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    name = data['name']
    threat = data['threat']
    lat = data['lat']
    lon = data['lon']

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO incidents(name,threat,latitude,longitude) VALUES(?,?,?,?)",
                (name, threat, lat, lon))

    conn.commit()
    conn.close()

    send_alert(name, threat, lat, lon)

    return jsonify({"status": "Alert Sent Successfully 🚨"})

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM incidents")
    data = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)