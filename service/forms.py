from flask_wtf import Form                                          # type: ignore
from wtforms.fields import StringField, PasswordField, RadioField, SubmitField   # type: ignore
from wtforms.validators import InputRequired, Length                     # type: ignore


class TitleSearchForm(Form):  # type: ignore
    search_term = StringField('search_term',
                              [InputRequired(message='Postcode is required')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


class LandingPageForm(Form):  # type: ignore
    information = RadioField('information', validators=[InputRequired(message='Please choose an option.')],
                             choices=[('title_summary', 'Title summary'), ('full_title_documents', 'Full title documents'), ('official_copy', 'Official copy')])

    submit = SubmitField("Continue")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
