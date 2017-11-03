from app import create_app
from config import config, blog_config


app = create_app(config, blog_config)
