from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateArticleLoginForm(FlaskForm):

    title1 = StringField('Main Title', validators=[DataRequired()])
    title2 = StringField('Secondary Title')
    content = TextAreaField()
    status = SelectField(
        'Status',
        choices=[('draft', 'Draft'), ('published', 'Published')]
    )


class EditArticleLoginForm(FlaskForm):

    title1 = StringField('Main Title', validators=[DataRequired()])
    title2 = StringField('Secondary Title')
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField()
    status = SelectField(
        'Status',
        choices=[('draft', 'Draft'), ('published', 'Published')]
    )
