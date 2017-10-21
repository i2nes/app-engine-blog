from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class ContactLoginForm(FlaskForm):

    name = StringField(label='name_', validators=[DataRequired()])
    email = StringField('email_', validators=[DataRequired()])
    message = TextAreaField('message_')
