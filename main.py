from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
import email_validator
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.environ.get('SECRET_KEY')

app.config.update(dict(
    MAIL_SERVER='smtp.googlemail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('USERNAME'),
    MAIL_PASSWORD=os.environ.get('PASSWORD')
))

mail = Mail(app)


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = TextAreaField(label='Message')
    submit = SubmitField(label="Send message")


@app.route("/", methods=['POST', 'GET'])
def home():
    cform = ContactForm()
    if cform.validate_on_submit():
        # print(f"Name:{cform.name.data}, E-mail:{cform.email.data}, message:{cform.message.data}")
        msg = Message(f"Message from {cform.email.data}", sender=f"{os.environ.get('USERNAME')}@gmail.com",
                      recipients=["krzysztof.jerzy.sztuk@gmail.com"])
        msg.body = f"{cform.name.data}\n{cform.message.data}"
        mail.send(msg)
        flash('Your message has been sent')
        return redirect(url_for('home'))
    return render_template("index.html", form=cform, now=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)

# TODO: na iphonie rozjeżdża się email, wiadomość flash i ikonki ze skillsów. Hamburger menu nie działa na Androidzie