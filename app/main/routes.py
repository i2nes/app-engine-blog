from . import app
from flask import render_template, abort
from config import blog_config
from app.models import Article
from google.appengine.ext import ndb
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


@app.route('/')
def home():

    context = {
        'title': 'Clean Blog - Start Bootstrap Theme',
    }

    q = Article.query().order(-Article.created)
    posts = q.fetch()

    return render_template('main/home_page.html', context=context, blog_config=blog_config, posts=posts)


@app.route('about/')
def about():

    context = {
        'title': 'About Page',
    }

    return render_template('main/about_page.html', context=context, blog_config=blog_config)


@app.route('contact/')
def contact():

    context = {
        'title': 'Contact Page',
    }

    return render_template('main/contact_page.html', context=context, blog_config=blog_config)


@app.route('blog/<slug>')
def post(slug):

    context = {
        'title': 'Post Page',
    }

    query = Article.query(ndb.AND(Article.slug == slug, Article.published == True)).fetch(1)

    if query:
        context['post_title_1'] = query[0].title1
        context['post_title_2'] = query[0].title2
        context['content'] = markdown.markdown(
            query[0].content,
            extensions=[GithubFlavoredMarkdownExtension()])
        context['created'] = query[0].created

        context['content'] = markdown.markdown(query[0].content, extensions=[GithubFlavoredMarkdownExtension()])
    else:
        abort(404)

    return render_template('main/post_page.html', context=context, blog_config=blog_config)


@app.app_errorhandler(404)
def page_not_found(e):

    context = {
        'title': 'Page Not Found',
    }

    return render_template('main/404.html', context=context, blog_config=blog_config), 404


@app.app_errorhandler(500)
def page_not_found(e):

    context = {
        'title': 'Server Error',
    }

    return render_template('main/500.html', context=context, blog_config=blog_config), 500
