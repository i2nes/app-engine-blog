from . import app
from flask import render_template, abort, redirect, url_for
from config import blog_config
from app.models import Article, ContactMessage
from google.appengine.ext import ndb
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import logging
from forms import ContactLoginForm


@app.route('/')
@app.route('page/<int:page_id>')
def home(page_id=1):

    context = {
        'title': blog_config['HOME_SEO_TITLE'],
        'meta_description': blog_config['HOME_SEO_DESCRIPTION'],
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

    # Check if there are any more posts for the next page
    if not q.fetch(offset=offset+blog_config['POSTS_LIST_LIMIT'], limit=1):
        context['next_page'] = None

    if posts:
        return render_template('main/home_page.html', context=context, blog_config=blog_config, posts=posts)
    else:
        abort(404)


@app.route('about/')
def about():

    context = {
        'title': 'About Page',
    }

    query = Article.query().order(Article.created)
    results = query.fetch(2)

    for result in results:
        if result.title1 == 'about_page':
            context['content'] = markdown.markdown(
                result.content,
                extensions=[GithubFlavoredMarkdownExtension()])
        else:
            logging.warn('About page content not found!')

    return render_template('main/about_page.html', context=context, blog_config=blog_config)


@app.route('contact/', methods=['GET', 'POST'])
def contact():

    context = {
        'title': 'Contact Page',
    }

    query = Article.query().order(Article.created)
    results = query.fetch(2)

    for result in results:
        if result.title1 == 'contact_page':
            context['content'] = markdown.markdown(
                result.content,
                extensions=[GithubFlavoredMarkdownExtension()])
        else:
            logging.warn('Contact page content not found!')

    form = ContactLoginForm()

    if form.validate_on_submit():

        msg = ContactMessage()

        msg.name = form.name.data
        msg.email = form.email.data
        msg.message = form.message.data

        msg.put()

        return redirect(url_for('main.contact'))

    else:
        pass

    return render_template('main/contact_page.html', context=context, form=form, blog_config=blog_config)


@app.route('blog/<slug>')
def post(slug):

    context = {
    }

    query = Article.query(ndb.AND(Article.slug == slug, Article.published == True))
    query = query.fetch()

    # Our URL slugging has no validation. Similar article titles may create duplicates.
    # All we are doing is logging a warning so that monitor and manually change duplicated slugs.
    if len(query) > 1:
        logging.warn('Duplicate Slug "{}". You should rename one of them to fix this issue'.format(slug))

    if query:
        context['post_title_1'] = query[0].title1
        context['post_title_2'] = query[0].title2
        context['post_author'] = query[0].author
        context['title'] = query[0].seo_title
        context['meta_description'] = query[0].seo_description
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


@app.route('tag/<tag>')
def tag_article_page(tag):

    context = {
        'title': 'Tags Page',
        'meta_description': 'Tags page',
    }

    q = Article.query(ndb.AND(Article.published == True, Article.tags == tag)).order(-Article.created)
    posts = q.fetch()

    if posts:
        return render_template('main/tags_page.html', context=context, blog_config=blog_config, posts=posts)
    else:
        abort(404)
