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

    # Comment out any social links you don't want to display
    'FACEBOOK_LINK': 'https://www.facebook.com/',
    'TWITTER_LINK': 'https://twitter.com/',
    'GITHUB_LINK': 'https://github.com/i2nes/app-engine-blog',

}
