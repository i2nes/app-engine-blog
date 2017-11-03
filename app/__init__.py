from flask import Flask
from app.models import Article, Feature
import logging


def create_app(config, blog_config):
    """This initiates the Flask app and starts your app engine instance.
    Startup Steps:
    1. Instantiate the Flask app with the config settings.
    2. Register bluprints.
    3. Create the Contact and About Pages in the datastore if they don't exist yet.
    4. Load the blog_config settings from the datatstore. Or add them if they don't exist yet.
    """

    logging.info('STARTUP: Getting ready to launch the Flask App')

    app = Flask(__name__)
    app.config.update(config)

    # Register blueprints

    logging.info('STARTUP: Register Blueprints')

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .editor import app as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')

    # Add Contact and About pages to the datastore when first launching the blog

    logging.info('STARTUP: Set up Contact and About pages')

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

    # Register blog configurations
    # The Blog is initially configured with blog_conf settings
    # The settings are added to the datastore and will take precedence from now on
    # You can change the settings in the datastore.
    # The settings are only updated on Startup, so you need to restart the instances to apply changes.

    logging.info('STARTUP: Register Blog Configurations')

    query = Feature.query()

    for feature in blog_config:

        # TODO: Add the accesslist to the datastore. The access list is still read only from the config file.
        if feature == 'EDITOR_ACCESS_LIST':
            pass

        # TODO: The posts limit is an int and needs to be converted. Find a better way of doing this.
        elif feature == 'POSTS_LIST_LIMIT':
            result = query.filter(Feature.title == feature).fetch()
            if result:

                logging.info('STARTUP: Loading {}'.format(result[0].title))

                blog_config['POSTS_LIST_LIMIT'] = int(result[0].value)

            else:

                logging.info('STARTUP: Adding to datastore: {}'.format(feature))

                f = Feature()
                f.title = feature
                f.value = str(blog_config[feature])
                f.put()

        # Load the configs or add them to the datastore if they don't exist yet
        else:
            result = query.filter(Feature.title == feature).fetch()
            if result:

                logging.info('STARTUP: Loading {}'.format(result[0].title))

                blog_config[result[0].title] = result[0].value

            else:

                logging.info('STARTUP: Adding to datastore: {}'.format(feature))

                f = Feature()
                f.title = feature
                f.value = blog_config[feature]
                f.put()

    # Startup complete
    logging.info('STARTUP: READY TO ROCK!!!')

    return app
