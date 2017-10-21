from . import app
from flask import render_template, url_for, redirect
from config import blog_config, config
from forms import CreateArticleLoginForm, EditArticleLoginForm
from app.models import Article, ContactMessage
from functools import wraps
from google.appengine.api import users
from socket import gethostname
import unicodedata
import re
import logging


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


@app.route('/messages/')
@login_required
def messages_page():

    context = {
        'logout_url': logout_url(),
        'title': 'Editor Messages',
    }

    query = ContactMessage().query().order(-Article.created)

    if query:
        context['messages'] = query.fetch()
    else:
        pass

    return render_template('editor/messages_page.html', context=context, blog_config=blog_config)


@app.route('/create/', methods=['GET', 'POST'])
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

        return redirect(url_for('editor.home'))

    else:
        pass

    return render_template('editor/create_article_page.html', context=context, form=form, blog_config=blog_config)


@app.route('/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):

    user = users.get_current_user()

    context = {
        'logout_url': logout_url(),
    }

    article = Article.get_by_id(article_id, parent=None)

    if not article:
        logging.info('Can not find article {} to edit'.format(article_id))
        return redirect(url_for('editor.home'))
    else:
        context['article_id'] = article_id

    form = EditArticleLoginForm()

    if form.validate_on_submit():

        article.title1 = form.title1.data
        article.title2 = form.title2.data
        article.slug = form.slug.data
        article.content = form.content.data
        article.published = True if form.status.data == 'published' else False

        article.put()

        return redirect(url_for('editor.home'))

    else:

        # Load post data from Datastore
        form.title1.data = article.title1
        form.title2.data = article.title2
        form.slug.data = article.slug
        form.content.data = article.content
        form.status.data = 'published' if article.published == True else 'draft'

    return render_template('editor/edit_article_page.html', context=context, form=form, blog_config=blog_config)


@app.route('/gallery')
@login_required
def thumbnails():

    context = {
        'logout_url': logout_url(),
        'title': 'Thumbnail Gallery',
    }

    return render_template('editor/image_gallery_page.html', context=context, blog_config=blog_config)
