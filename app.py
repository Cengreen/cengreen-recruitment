
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
from flask import Flask, request, render_template_string, send_file
import datetime

app = Flask(__name__)

APPLICATION_CSV = "applications.csv"
GMAIL_USER = "cengreenuk@gmail.com"
GMAIL_PASSWORD = "cjgc bajl lyxs ovmo"

ADMIN_EMAIL = "cengreenuk@gmail.com"
SENDER_NAME = "Cengreen Recruitment Team"

AUTO_REPLY_MESSAGE = """
Thank you for applying. We will review your application and contact you soon.
"""

HTML_FORM = '''
    <h2>Job Application Form</h2>
    <form method="POST">
      Name: <input name="name"><br>
      Email: <input name="email"><br>
      Phone: <input name="phone"><br>
      Position Applied: <input name="position"><br>
      CV Link: <input name="cv"><br>
      <button type="submit">Submit</button>
    </form>
    <br>
    <a href="/admin">Go to Admin Page</a>
'''

ADMIN_PAGE_TEMPLATE = '''
    <h2>Applications Admin Page</h2>
    <a href="/export">Download CSV</a><br><br>
    <table border="1">
      <tr><th>Name</th><th>Email</th><th>Phone</th><th>Position</th><th>CV</th><th>Date</th></tr>
      {% for row in rows %}
      <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td><td>{{ row[3] }}</td><td><a href="{{ row[4] }}">CV</a></td><td>{{ row[5] }}</td></tr>
      {% endfor %}
    </table>
'''

def send_email(to, subject, message):
    msg = MIMEMultipart()
    msg['From'] = f"{SENDER_NAME} <{GMAIL_USER}>"
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        cv = request.form['cv']
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save to CSV
        with open(APPLICATION_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, phone, position, cv, date])

        # Notify admin
      try:
    send_email(ADMIN_EMAIL, f"New Application: {name}", f"{name} applied for {position}.\nEmail: {email}\nPhone: {phone}\nCV: {cv}")
    send_email(email, "Thank you for your application", AUTO_REPLY_MESSAGE)
except Exception as e:
    print("Email error:", e)

        return "Application submitted successfully! <a href='/'>Submit another</a>"

    return HTML_FORM

@app.route('/admin')
def admin():
    with open(APPLICATION_CSV, newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return render_template_string(ADMIN_PAGE_TEMPLATE, rows=rows)

@app.route('/export')
def export():
    return send_file(APPLICATION_CSV, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
