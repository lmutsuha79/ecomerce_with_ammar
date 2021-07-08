from . import app, login_manager
from flask import render_template, request, redirect, url_for, jsonify
from .form import RegistrationForm, LoginForm
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
    form = LoginForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    return redirect(url_for('home_page'))
                form.new_errors = {'password': ['Not valid']}
            else:
                form.new_errors = {'username': ['not found user']}

    return render_template('sing_in.html', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    static = True
    form = RegistrationForm(request.form)
    # if current_user.is_authenticated:
    #     return redirect(url_for('home_page'))

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            if username and User.query.filter_by(username=username).first():
                form.new_errors = {'username': [
                    'This username exist enter other one']}
                static = False

            if not email:
                form.new_errors = {'email': ['Not valid']}
                static = False

            if not password:
                form.new_errors = {'password': ['Not valid']}
                static = False

            if static:
                u1 = User(username=username,
                          email=email,
                          password=password)

                db.session.add(u1)
                db.session.commit()
                login_user(u1)
                return redirect(url_for('home_page'))
                # 204

    return render_template('sing_up.html', form=form)


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


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404_page.html'), 404


@app.route('/games')
def games():
    return render_template('games.html')



@app.route('/one_game_page')
def one_game_page():
    return render_template('one_game_page.html')