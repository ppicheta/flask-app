from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'myapp12'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "neonrobot9@gmail.com"
app.config['MAIL_PASSWORD'] = "odjq dncr tboo spfd"
db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
    

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        occupation = request.form['occupation']
        date_given = request.form['date']
        date_obj = datetime.strptime(date_given, '%Y-%m-%d')

        form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        message_body = 'Thank you for your submission'
        message = Message(subject='New form submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=message_body)
        mail.send(message)
        flash(f'{first_name}, your form submitted succesfully','success')

    return render_template("index.html") 


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)