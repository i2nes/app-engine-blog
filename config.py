import os


config = {
    'DEBUG': not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'),
    'SECRET_KEY': 'Some big sentence',
}