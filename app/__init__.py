from flask import Flask
from app.models import Article
import logging


def create_app(config_name):

    logging.info('Getting ready to launch the Flask App')

    app = Flask(__name__)
    app.config.update(config_name)

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .editor import app as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')

    # If no Datastore entity has been created yet, in other words,
    # if the blog app was never run, we'll create the first two entities
    # The first two entities will be used for the about and contact
    # pages content.

    # Query for content in the Datastore
    query = Article.query().order(-Article.created)
    results = query.fetch(1)

    logging.info('Checking if any posts exist: {} found'.format(len(results)))

    # If no content exists, we'll create the first entries
    if not results:

        logging.info('No content found. Creating default About and Contact Pages.')

        about_page = Article()
        about_page.title1 = 'about_page'
        about_page.slug = 'about-page'
        about_page.author = ''
        about_page.content = 'About page'
        about_page.published = False

        contact_page = Article()
        contact_page.title1 = 'contact_page'
        contact_page.slug = 'contact-page'
        contact_page.author = ''
        contact_page.content = 'Contact page'
        contact_page.published = False

        about_page.put()
        contact_page.put()

    # Startup complete
    logging.info('READY TO ROCK!!!')

    return app
