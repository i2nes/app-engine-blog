from flask import Flask
from app.models import Article
import logging


def create_app(config_name):

    logging.info('STARTUP: Getting ready to launch the Flask App')

    app = Flask(__name__)
    app.config.update(config_name)

    # Register blueprints

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .editor import app as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')

    # Add Contact and About pages to the datastore when first launching the blog

    # Contact page creation
    query = Article.query(Article.slug == 'contact-page')
    result = query.fetch(1)

    if result:
        logging.info('STARTUP: Contact page exists')
    else:
        logging.info('STARTUP: Creating a contact page')
        contact_page = Article()
        contact_page.title1 = 'Contact Me'
        contact_page.title2 = 'Have questions? I have answers (maybe).'
        contact_page.slug = 'contact-page'
        contact_page.author = ''
        contact_page.content = 'Want to get in touch with me? Fill out the form below to send me a message and I ' \
                               'will try to get back to you within 24 hours! '
        contact_page.published = False
        contact_page.put()

    # About page creation
    query = Article.query(Article.slug == 'about-page')
    result = query.fetch(1)

    if result:
        logging.info('STARTUP: About page exists')
    else:
        logging.info('STARTUP: Creating an about page')
        about_page = Article()
        about_page.title1 = 'About Me'
        about_page.title2 = 'This is what I do.'
        about_page.slug = 'about-page'
        about_page.author = ''
        about_page.content = ''
        about_page.published = False
        about_page.put()

    # Startup complete
    logging.info('STARTUP: READY TO ROCK!!!')

    return app
