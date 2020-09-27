import os
import base64
import peewee
from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
# app.secret_key = b'\x11\x14\x17\x8a\xf8@\x03\xf0\xf9U[\x93"\xfb\x94\x00\x7fGN\xad\x8a~\xb3\x8f'
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    # session['donation_amount']

    if 'donation_amount' not in session:
        session['donation_amount'] = 0
    
    #session['donor_name']
    if 'donor_name' not in session:
        session['donor_name'] = 'XXXX'

    if request.method == 'POST':
        amount = int(request.form['amount'])
        fullname = request.form['fullname']
        session['donation_amount'] = amount
        session['donor_name'] = fullname

    return render_template('donate.jinja2', session=session)


@app.route('/save', methods=['POST'])
def save():
    donate()
    code = base64.b32encode(os.urandom(8)).decode().strip("=")

    donor_name = session.get('donor_name', 'XXXX')
    donor_id = 0

    try:
        donor = Donor.get(Donor.name == donor_name)

        if donor:
            donor_id = donor
        
        amount = session.get('donation_amount', 0)

        save_donation = Donation(value=amount, donor_id=donor_id)
        save_donation.save()
    except peewee.DoesNotExist as missing:
        print("\nDonor is not found! ", missing)

    return render_template('save.jinja2', code=code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
