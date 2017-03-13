"""Security configurations."""

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Everyone, Authenticated
from pyramid.security import Allow
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import SignedCookieSessionFactory


def check_credentials(username, password):
    """Check credentials."""
    stored_username = os.environ.get('AUTH_USERNAME', '')
    stored_password = os.environ.get('AUTH_PASSWORD', '')
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password,
                                                      stored_password)
            except ValueError:
                # ValueError is raised if the stored password
                # is not hashed or if the salt is improper
                pass
    return is_authenticated


class MyRoot(object):
    """MyRoot."""

    def __init__(self, request):
        """Init for MyRoot Class."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit'),
        (Allow, Authenticated, 'create'),
    ]


def includeme(config):
    """Security-related configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'blahblah')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)
    session_secret = os.environ.get('SESSION_SECRET', 'blahblah')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
