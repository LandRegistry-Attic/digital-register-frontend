from wtforms.fields import StringField, PasswordField
from wtforms.validators import Required, Length
from flask_wtf import Form


class SigninForm(Form):
    username = StringField('username', [Required(message='Username is required'),
                                        Length(min=4, max=70, message='Username is incorrect')])
    password = PasswordField('password', [Required(message='Password is required')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class TitleSearchForm(Form):
    search_term = StringField('search_term',
                              [Required(message='Search term is required'),
                               Length(min=3, max=70, message='Search term is too short/long')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
