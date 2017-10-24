from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateArticleLoginForm(FlaskForm):

    title1 = StringField('Main Title', validators=[DataRequired()])
    title2 = StringField('Secondary Title')
    seo_title = StringField('SEO Title')
    seo_description = StringField('SEO Description')
    content = TextAreaField()
    tags = StringField('Tags')
    status = SelectField(
        'Status',
        choices=[('draft', 'Draft'), ('published', 'Published')]
    )


class EditArticleLoginForm(FlaskForm):

    title1 = StringField('Main Title', validators=[DataRequired()])
    title2 = StringField('Secondary Title')
    slug = StringField('Slug', validators=[DataRequired()])
    seo_title = StringField('SEO Title')
    seo_description = StringField('SEO Description')
    content = TextAreaField()
    tags = StringField('Tags')
    status = SelectField(
        'Status',
        choices=[('draft', 'Draft'), ('published', 'Published')]
    )
