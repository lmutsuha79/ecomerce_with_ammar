from wtforms import SubmitField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(),])

    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._errors = dict()

    @property
    def new_errors(self):
        self._errors.update(self.errors)
        return self._errors

    @new_errors.setter
    def new_errors(self, error):
        self._errors.update(error)


class RegistrationForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(min=2)])

    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Password should be at least %(min)d characters long')])

    confirm_ = PasswordField(label='Confirm Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Both password fields must be equal!')])

    submit = SubmitField('Create Account')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self._errors = dict()

    @property
    def new_errors(self):
        self._errors.update(self.errors)
        return self._errors

    @new_errors.setter
    def new_errors(self, error):
        self._errors.update(error)
