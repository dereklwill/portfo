from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)

import smtplib
from email.message import EmailMessage

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

name1 = 'Old Name'
subject1 = 'Old Subject'
message1 = 'Old Message'

def write_to_csv(data):
    with open('database.csv', newline='', mode= 'a') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            email1 = EmailMessage()
            email1['from'] = 'Website Contact Form'
            email1['to'] = 'WilliamsonITBot@gmail.com'
            email1['subject'] = 'From: ' + data['email'] + ' Message: ' + data['subject']
            email1.set_content(data['message'])
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('WilliamsonITBot@gmail.com', 'Vivi1576!')
                smtp.send_message(email1)
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong, try again'