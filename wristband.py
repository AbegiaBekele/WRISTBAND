from flask import Flask, render_template, request, redirect, url_for, session
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your_secret_key'

TWILIO_ACCOUNT_SID = 'AC44c0084cbaad95a2384e0d473f639c0b'
TWILIO_AUTH_TOKEN = 'd60871906d886611ad3c7c523cb41bdb'
TWILIO_PHONE_NUMBER = '+18583467844'
RECIPIENT_PHONE_NUMBER = '+48576226010'

LOGIN_CREDENTIALS = {'abegiabekele': '21543825'}

class Wristband:
    def init(self):
        self.temperature = 0
        self.oxygen_level = 0
        self.pulse_rate = 0

@app.route('/')
def index():
    if 'logged_in' in session:
        wristband = Wristband()  
        return render_template('index.html', wristband=wristband)  # Pass wristband to the template
    else:
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in LOGIN_CREDENTIALS and LOGIN_CREDENTIALS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/get_wristband_data')
def get_wristband_data():
    if 'logged_in' in session:
        wristband = Wristband()
        wristband.temperature = 41.2
        wristband.oxygen_level = 90
        wristband.pulse_rate = 85

        if wristband.temperature > 40:
            report("Temperature is above 40°C!")
        if wristband.oxygen_level < 92:
            report("Oxygen level is below 92%!")
        if wristband.pulse_rate > 80:
            report("Pulse rate is above 80 BPM!")

        return render_template('index.html', wristband=wristband)
    else:
        return redirect(url_for('login'))

def report(message):
    send_sms_alert(message)

def send_sms_alert(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        client.messages.create(
            to=RECIPIENT_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print("SMS Alert Sent Successfully!")
    except Exception as e:
        print("Failed to send SMS alert:", str(e))

if __name__ == "__main__":
    app.run(debug=True)