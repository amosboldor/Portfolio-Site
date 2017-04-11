"""Views for profolio app."""
import datetime
import json

import markdown
from bs4 import BeautifulSoup
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError

from ..models import BlogPost
from ..security import check_credentials
from pyramid_mailer.message import Message
from pyramid.httpexceptions import HTTPNotFound


def get_summary(html):
    """Return summary portion of BlogPost."""
    soup = BeautifulSoup(html, "html5lib")
    if not soup.summary:
        return html
    return str(soup.summary)


@view_config(route_name="posts",
             renderer="../templates/posts.jinja2",
             permission="view")
def posts(request):
    """View for listing all the posts."""
    try:
        query = request.dbsession.query(BlogPost)
        posts = []
        for x in query.all()[::-1]:
            posts.append({
                "title": x.title,
                "date": str(x.date),
                "summary": get_summary(x.html),
                "id": x.id
            })
    except DBAPIError:
        return Response('It don\'t work right.', content_type='text/plain', status=500)
    return {'posts': posts}


@view_config(route_name="detail",
             renderer="../templates/post.jinja2",
             permission="view")
def detail(request):
    """View for the detail page."""
    query = request.dbsession.query(BlogPost)
    post = query.filter(BlogPost.id == request.matchdict['id']).first()
    if post:
        return {"post": post}
    return HTTPNotFound()


@view_config(route_name="create",
             renderer="json",
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
            new_model = BlogPost(title=title, body=request.POST["body"], html=html, date=date)
            request.dbsession.add(new_model)
            id = request.dbsession.query(BlogPost).filter(BlogPost.title == title).first().id
            return {"id": id}
    return {}


@view_config(route_name="update",
             permission="update")
def update(request):
    """View for update page."""
    if request.method == "POST":
        title = request.POST["title"]
        html = markdown.markdown(request.POST["body"],
                                 extensions=['codehilite', 'tables'])
        query = request.dbsession.query(BlogPost)
        post_dict = query.filter(BlogPost.id == request.matchdict['id'])
        post_dict.update({"title": title,
                          "body": request.POST["body"],
                          "html": html})
        return HTTPFound(location=request.route_url('home'))
    return {}


@view_config(route_name='home',
             renderer='../templates/home.jinja2',
             permission="view")
def home(request):
    """Home Page View."""
    return {}


@view_config(route_name='login',
             renderer='../templates/login.jinja2',
             require_csrf=False,
             permission="view")
def login(request):
    """Login View."""
    if request.method == 'POST':
        username = request.params.get('Username', '')
        password = request.params.get('Password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('posts'),
                             headers=headers)
    return {}


@view_config(route_name='logout',
             permission="view")
def logout(request):
    """Logout view."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name="api_list",
             renderer="json",
             permission="view")
def api_list_view(request):
    """JSON."""
    posts = request.dbsession.query(BlogPost).all()
    output = [item.to_json() for item in posts]
    if output:
        return output
    return HTTPNotFound()


@view_config(route_name="api_post",
             renderer="json",
             permission="view")
def api_post_view(request):
    """JSON."""
    query = request.dbsession.query(BlogPost)
    post = query.filter(BlogPost.id == request.matchdict['id']).first()
    if post:
        if request.params.get('summary') == 'True':
            return json.dumps({"summary": get_summary(post.html)})
        post = post.to_json()
        return post
    return HTTPNotFound()


@view_config(route_name="email",
             renderer="json",
             require_csrf=False,
             permission="view")
def hire_me(request):
    """Send email and text for hire me button."""
    if request.method == "POST":
        post_dict_keys = list(request.POST.keys())
        if "email" in post_dict_keys and "body" in post_dict_keys and "subject" in post_dict_keys:
            email = request.POST["email"]
            html = markdown.markdown(request.POST["body"],
                                     extensions=['tables'])
            subject = request.POST["subject"]
            message = Message(subject=subject,
                              sender='admin@mysite.com',
                              recipients=["amosboldor@gmail.com"],
                              body=email + '\n' + html)
            request.mailer.send(message)
            return {}
    return {}


@view_config(route_name='projects',
             renderer='../templates/projects.jinja2',
             permission='view')
def projects(request):
    """Display projects."""
    return {}


@view_config(route_name='delete',
             permission='delete')
def delete_post(request):
    """Delete a blog post."""
    if request.method == "DELETE":
        query = request.dbsession.query(BlogPost)
        post = query.filter(BlogPost.id == request.matchdict['id']).first()
        request.dbsession.delete(post)
        return HTTPFound(location=request.route_url('home'))
    return {}
