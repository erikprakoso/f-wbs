from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home.index'))
    if request.method == 'POST':
        email = request.form['email']
        print("email", email)
        password = request.form['password']
        print("password", password)

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home.index'))

        flash('Incorrect email or password. Please try again.', 'error')
        return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        age = request.form['age']
        institute = request.form['institute']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        else:
            user = User(email, name, age, institute, password)
            if user.save():
                login_url = url_for('auth.login')  # Get the login URL
                flash(f'Registration successful. Please <a href="{login_url}">login</a> to continue.', 'success')
                return redirect(url_for('auth.register'))
            else:
                flash('Something went wrong. Please try again.', 'error')
                return render_template('register.html')

    return render_template('register.html')



@auth_bp.route('/logout')
def logout():
    session.pop('email', None)  # Menghapus session 'email'
    return redirect(url_for('auth.login')) 