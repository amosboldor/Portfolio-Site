"""Views for profolio app."""
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember, forget
from ..security import check_credentials
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound
from ..models import BlogPost
import datetime
import markdown
import html2text


@view_config(route_name="posts", renderer="../templates/posts.jinja2")
def posts(request):
    """View for listing all the posts."""
    try:
        query = request.dbsession.query(BlogPost)
    except DBAPIError:
        return Response('It don\'t work right.', content_type='text/plain', status=500)
    return {'posts': query.all()[::-1]}


@view_config(route_name="detail", renderer="../templates/post.jinja2")
def detail(request):
    """View for the detail page."""
    query = request.dbsession.query(BlogPost)
    post = query.filter(BlogPost.id == request.matchdict['id']).first()
    return {"post": post}


@view_config(route_name="create",
             permission="create")
def create(request):
    """View for new BlogPost page."""
    if request.method == "POST":
        post_dict_keys = list(request.POST.keys())
        if "title" in post_dict_keys and "body" in post_dict_keys:
            title = request.POST["title"]
            html = markdown.markdown(request.POST["body"],
                                     extensions=['codehilite', 'tables'])
            date = datetime.date.today()
            new_model = BlogPost(title=title, body=html, date=date)
            request.dbsession.add(new_model)
            return HTTPFound(location=request.route_url('home'))
    return {}


@view_config(route_name="update",
             # renderer="../templates/edit_BlogPost.jinja2",
             permission="edit")
def update(request):
    """View for update page."""
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        date = datetime.date.today()
        query = request.dbsession.query(BlogPost)
        post_dict = query.filter(BlogPost.id == request.matchdict['id'])
        post_dict.update({"title": title,
                          "body": body,
                          "date": date})
        return HTTPFound(location=request.route_url('home'))
    query = request.dbsession.query(BlogPost)
    post_dict = query.filter(BlogPost.id == request.matchdict['id']).first()
    ## html2text
    import pdb; pdb.set_trace()
    return {"post": post_dict}


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


@view_config(route_name="api_list", renderer="json")
def api_list_view(request):
    """JSON."""
    posts = request.dbsession.query(BlogPost).all()
    output = [item.to_json() for item in posts]
    return output


@view_config(route_name="api_post", renderer="json")
def api_post_view(request):
    """JSON."""
    query = request.dbsession.query(BlogPost)
    post = query.filter(BlogPost.id == request.matchdict['id']).first()
    return post.to_json()
