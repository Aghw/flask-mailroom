import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation 

app = Flask(__name__)
app.secret_key = b'\x11\x14\x17\x8a\xf8@\x03\xf0\xf9U[\x93"\xfb\x94\x00\x7fGN\xad\x8a~\xb3\x8f'


@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 6738))
#     app.run(host='0.0.0.0', port=port)


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
    
    # amount = session.get('donation_amount', 0)
    amount = session.get('donation_amount', 0)

    save_donation = Donation(value=amount, donor_id=2)
    save_donation.save()

    return render_template('save.jinja2', code=code)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
