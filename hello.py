from flask import Flask, render_template, flash, redirect
import os

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, InputRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkeyiwillhideit:)"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'users.db')


######### FORM ################
class NamerForm(FlaskForm):
    name = StringField('Enter your name:', validators=[DataRequired()])
    age = IntegerField('Enter your age:')
    submit = SubmitField('Register')

class UserForm(FlaskForm):
    name = StringField('Enter your Name:', validators=[DataRequired()])
    email = EmailField('Enter your Email:', validators=[DataRequired()])
    submit = SubmitField('Register User')

####### DATABASE ##############
db = SQLAlchemy(app)

class UsersDb(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False )
    email = db.Column(db.String, nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.name} and email:{self.email}'


############## VIEWS #######################
@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

@app.route("/user/add", methods=['GET', 'POST'])
def add_user_to_db():
    form = UserForm()
    name = None
    email = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        # querying the db if the email is already present
        user = UsersDb.query.filter_by(email=email).first()
        if user:
            flash(f'{email} already exists. Try logging-in')
        else:
            new_user = UsersDb(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash(f'{name} with {email} was registered successfully!')           

        form = UserForm(formdata=None)
    
    # quering all users and ordering with date_added
    disp_all_users = UsersDb.query.order_by(UsersDb.date_added)

    return render_template('add-user-to-db.html', form=form, name=name, email=email, disp_all_users=disp_all_users)

@app.route("/name", methods=['GET', 'POST'])
def enter_name():
    name = None
    age = None
    form = NamerForm()

    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data

        form=NamerForm(formdata=None)
        flash(f'{name} was registered successfully!')

        
        # return redirect(url_for('enter_name'))

    return render_template('name.html', form=form, name=name, age=age)




###### custom error page

# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def internal_server_e(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)