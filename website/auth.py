from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

# ---------------- Login ----------------
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:   # ✅ plain text password check
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


# ---------------- Logout ----------------
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ---------------- Sign Up ----------------
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        first_name = request.form.get('firstName').strip()
        password1 = request.form.get('password1').strip()
        password2 = request.form.get('password2').strip()

        # Validation checks
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif not re.search(r'[A-Z]', password1) or not re.search(r'[0-9]', password1):
            flash('Password must include at least 1 uppercase letter and 1 number.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=password1   # ✅ saving raw password (no hashing)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
