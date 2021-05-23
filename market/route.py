from market import app, login_manager
from flask import render_template, request, redirect, url_for, flash
from market.model import db, User
from flask_login import login_user, current_user, login_required, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
def profile_page():
    return 'Profile'


@app.route('/')
def home_page():
    return 'HOme'


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form.get("username",)
        password = request.form.get("password",)
        print(username, password)
    #     if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('home_page'))
            print('wronge user')
        print('not found')

    return render_template('sing_in.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        print('post')
        static = True
        username = request.form.get("username",)
        email = request.form.get("email",)
        password = request.form.get("password",)
        if User.query.filter_by(username=username).first():
            print('found')
            static = False
        if User.query.filter_by(email=email).first():
            print('found')
            static = False

        if static:
            u1 = User(username=username,
                      email=email,
                      password=password)

            db.session.add(u1)
            db.session.commit()
            login_user(u1)
            print('done')
            return redirect(url_for('home_page'))

    return render_template('sing_up.html')


@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('login_page'))


@app.route('/recovery')
def recovery_page():
    return 'Recovery'
