"""Views for profolio app."""
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    """Home Page View."""
    return {}
