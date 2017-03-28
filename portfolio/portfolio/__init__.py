"""The main function."""
from pyramid.config import Configurator
import os


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    if "sqlalchemy.url" not in settings:
        sql_url = os.environ.get('DATABASE_URL', 'sqlite:///BlogPostDB.sqlite')
        settings["sqlalchemy.url"] = sql_url
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
