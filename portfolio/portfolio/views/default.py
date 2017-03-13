"""Views for profolio app."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember, forget
from ..security import check_credentials
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    """Home Page View."""
    return {}


@view_config(route_name='login',
             renderer='../templates/login.jinja2',
             require_csrf=False)
def login(request):
    """Login View."""
    if request.method == 'POST':
        username = request.params.get('Username', '')
        password = request.params.get('Password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'),
                             headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    """Logout view."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
