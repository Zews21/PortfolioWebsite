from flask import Flask, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_ckeditor import CKEditor
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_ckeditor import CKEditorField

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management and CSRF protection
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

# Flask-Mail configuration for sending emails through Gmail's SMTP server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEBUG'] = False

# Initialize extensions
ckeditor = CKEditor(app)  # Rich text editor for forms
mail = Mail(app)  # Flask-Mail instance for handling emails

# List of projects, hard-coded in the script for easier editing since the list is small
projects = [
    {
        "title": "Blog",
        "description": "Conceptual blog website built with Flask, WTForms, SQLAlchemy and Bootstrap.",
        "image": "images/project1.jpg",
        "link": "https://github.com/yourusername/project1"
    },
    {
        "title": "Dino Game Bot",
        "description": "A bot that plays the Chrome Dino game, built with pyautogui.",
        "image": "images/project2.jpg",
        "link": "https://github.com/yourusername/project2"
    },
    {
        "title": "Space Invaders Clone",
        "description": "An simplified, OOP approach to the Space Invaders game, built using Turtle.",
        "image": "images/project3.jpg",
        "link": "https://github.com/yourusername/project3"
    }
]


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = CKEditorField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")


# Route for the about page
@app.route("/about")
def about():
    return render_template("about.html")


# Route for the portfolio page, passing project data to the template
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", projects=projects)


# Route for the contact page with form handling
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Gather form data for the email message
        name = form.name.data
        sender_email = form.email.data
        subject = form.subject.data
        message = form.message.data

        # Construct the email message
        msg = Message(subject=subject,
                      sender=os.environ.get("MAIL_USERNAME"),
                      recipients=[os.environ.get("MAIL_USERNAME")])
        msg.body = f"Message from {name} ({sender_email}):\n\n{message}"

        try:
            # Attempt to send the email
            mail.send(msg)
            flash('Thank you for your message! I will get back to you soon.', 'success')
        except Exception as e:
            # Log and display an error if email fails
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            print(f"Error: {e}")

        return redirect(url_for('contact'))  # Redirect to prevent form resubmission

    return render_template("contact.html", form=form)


# Run the Flask app in debug mode for development
if __name__ == "__main__":
    app.run()
