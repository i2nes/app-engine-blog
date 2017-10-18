from . import app
from flask import render_template, url_for, redirect
from config import blog_config, config
from forms import CreateArticleLoginForm
from app.models import Article
from functools import wraps
from google.appengine.api import users
from socket import gethostname
import unicodedata
import re


# Functions
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = users.get_current_user()
        if user is None:
            return redirect(users.create_login_url(url_for('editor.home')))  # Go to login page
        elif user.email() in [email for email in blog_config['EDITOR_ACCESS_LIST']]:
            return f(*args, **kwargs)
        else:
            return redirect(users.create_login_url(url_for('main.home')))

    return decorated_function


def logout_url():
    # Fix for logout. Googles create_logout_url api logs the user out of all
    # his google accounts, instead of only logging out of our app.
    # https://bugs.chromium.org/p/chromium/issues/detail?id=162590
    # In DEV we can use create_logout_url in Prod we have to hack the url
    if config['DEBUG']:
        logout = users.create_logout_url(url_for('main.home'))
    else:
        logout = '/_ah/logout?continue=https://' + gethostname() + '/'
    return logout


def slugify(s):
    slug = unicodedata.normalize('NFKD', s)
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug


# Editor Routes

@app.route('/')
@login_required
def home():

    context = {
        'logout_url': logout_url(),
        'title': 'Editor Home Page',
    }

    query = Article.query().order(-Article.created)

    if query:
        context['posts'] = query.fetch()
    else:
        pass

    return render_template('editor/home_page.html', context=context, blog_config=blog_config)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():

    user = users.get_current_user()

    context = {
        'logout_url': logout_url(),
    }

    form = CreateArticleLoginForm()
    if form.validate_on_submit():

        new_article = Article()

        new_article.title1 = form.title1.data
        new_article.title2 = form.title2.data
        new_article.author = blog_config['EDITOR_ACCESS_LIST'][user.email()]
        new_article.slug = slugify(form.title1.data)
        new_article.content = form.content.data
        new_article.published = True if form.status.data == 'published' else False

        new_article.put()

        return redirect(url_for('main.home'))

    else:
        pass

    return render_template('editor/create_article_page.html', context=context, form=form, blog_config=blog_config)

