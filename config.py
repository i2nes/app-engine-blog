import os


config = {
    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}
