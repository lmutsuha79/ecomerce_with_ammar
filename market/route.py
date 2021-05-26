from . import app, login_manager
from flask import render_template, request, redirect, url_for, jsonify, session
from .model import db, User
from flask_login import login_user, current_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
def profile_page():
    return 'Profile'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    errors = None
    print(request.method)
    if request.method == 'POST':
        username = request.form.get("username", )
        password = request.form.get("password", )

        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('home_page'))

        errors = 'wrong input'

    return render_template('sing_in.html', errors=errors)


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    errors = dict()
    # if current_user.is_authenticated:
    #     return redirect(url_for('home_page'))

    if request.method == 'POST':
        username = request.form.get("username", )
        email = request.form.get("email", )
        password = request.form.get("password", )
        if User.query.filter_by(username=username).first():
            errors['username'] = 'user exist'

        else:
            u1 = User(username=username,
                      email=email,
                      password=password)

            db.session.add(u1)
            db.session.commit()
            login_user(u1)
            print('done')
            return redirect(url_for('home_page'))
            # 204

    return render_template('sing_up.html', errors=errors)


@app.route('/check-reg', methods=['POST'])
def check_user_mail():
    field_ = request.form.get('username')
    if field_:
        if User.query.filter_by(username=field_).first():
            return jsonify(result=False)

    return jsonify(result=True)


@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('login_page'))


@app.route('/recovery')
def recovery_page():
    return 'Recovery'
