# Before uploading to app engine you must setup your own
# Blog Configurations and SECRET_KEY
# Then save and rename this file to config.py
import os

# Flask App Configurations
config = {

    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}

# Blog Configurations
blog_config = {

    'BLOG_NAME': 'Start Bootstrap',
    'BLOG_TITLE_LINE_1': 'Clean Blog',
    'BLOG_TITLE_LINE_2': 'A Blog Theme by Start Bootstrap',
    'COPYRIGHT': 'Your Website 2017',
    'POST_AUTHOR': 'Start Bootstrap',
    'POST_AUTHOR_LINK': '#',
    'POSTS_LIST_LIMIT': 5,

    # Blog Images
    'IMG_ABOUT': 'img/about-bg.jpg',
    'IMG_CONTACT': 'img/contact-bg.jpg',
    'IMG_HOME': 'img/home-bg.jpg',
    'IMG_POST': 'img/post-bg.jpg',

    # Comment out any social links you don't want to display
    'FACEBOOK_LINK': 'https://www.facebook.com/',
    'TWITTER_LINK': 'https://twitter.com/',
    'GITHUB_LINK': 'https://github.com/i2nes/app-engine-blog',
    'LINKEDIN_LINK': 'https://www.linkedin.com/',
    'INSTAGRAM_LINK': 'https://www.instagram.com/',

    # Authorized Gmail Accounts
    # Only these users will be able to access /editor for editing posts
    'EDITOR_ACCESS_LIST': {
        'email1@gmail.com': 'John Doe',
        'email2@gmail.com': 'Jane Doe',
    }

}
