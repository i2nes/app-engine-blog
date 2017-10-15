from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateArticleLoginForm(FlaskForm):

    title1 = StringField('Title 1', validators=[DataRequired()])
    title2 = StringField('Title 2', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField()
    status = SelectField(
        'Status',
        choices=[('draft', 'Draft'), ('published', 'Published')]
    )
