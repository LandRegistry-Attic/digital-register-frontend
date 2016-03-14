from flask_wtf import Form                             # type: ignore
from wtforms.fields import StringField, PasswordField  # type: ignore
from wtforms.validators import Required, Length        # type: ignore


class TitleSearchForm(Form):  # type: ignore
    search_term = StringField('search_term',
                              [Required(message='Search term is required'),
                               Length(min=3, max=70, message='Search term is too short/long')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
