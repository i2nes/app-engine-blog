from . import app
from flask import render_template, abort
from config import blog_config
from app.models import Article
from google.appengine.ext import ndb
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


@app.route('/')
@app.route('page/<int:page_id>')
def home(page_id=1):

    context = {
        'title': 'Clean Blog - Start Bootstrap Theme',
    }

    if page_id < 1:
        abort(404)
    elif page_id > 1:
        context['previous_page'] = page_id - 1

    context['next_page'] = page_id + 1
    page_id -= 1  # This makes the home page and page 1, instead of page 0

    # For now we'll use offset and limit in fetch() to page through posts
    # This has some drawbacks
    # 1. You are paying for reading all the entities that you are skipping
    # 2. This method is limited to 1000 posts.
    # TODO: Refactor to use cursors instead of offset. See:
    # https://groups.google.com/forum/#!topic/google-appengine/4ccIisoxYpc
    # TODO: Remove the next page link from the last page, it links to a 404

    offset = page_id * blog_config['POSTS_LIST_LIMIT']
    q = Article.query(Article.published == True).order(-Article.created)
    posts = q.fetch(offset=offset, limit=blog_config['POSTS_LIST_LIMIT'])

    if posts:
        return render_template('main/home_page.html', context=context, blog_config=blog_config, posts=posts)
    else:
        abort(404)


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

        # TODO: Find a way of doing this better with css or in the markdown.
        # Adding the "img-fluid" class for having responsive images
        context['content'] = context['content'].replace('<img', '<img class="img-fluid"')
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
