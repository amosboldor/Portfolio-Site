"""Testing File."""
import datetime
import unittest

import transaction
from portfolio.models import get_tm_session
from portfolio.models.meta import Base
from pyramid import testing
from webtest import TestApp


def dummy_request(dbsession):
    """Return Dummy Request."""
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    """Base Test with db setup."""

    def setUp(self):
        """Setup the db."""
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('..models')
        self.config.include('..routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        """Init Database."""
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        Base.metadata.create_all(engine)

    @staticmethod
    def tear_down():
        """Teardown and abort."""
        testing.tearDown()
        transaction.abort()


class TestViewsSuccessCondition(unittest.TestCase):
    """Test Views Success Condition."""

    @classmethod
    def setUp(cls):
        """Add to database."""
        from portfolio.models.meta import Base
        from portfolio import main
        from portfolio.models import (
            get_tm_session,
            BlogPost
        )

        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:'
        }
        app = main({}, **settings)
        cls.testapp = TestApp(app)

        session_factory = app.registry['dbsession_factory']
        cls.engine = session_factory.kw['bind']
        Base.metadata.create_all(bind=cls.engine)

        with transaction.manager:
            dbsession = get_tm_session(session_factory, transaction.manager)
            model = BlogPost(
                title='Test Title',
                body='Test Body',
                html='<p>Test Body</p>',
                date=datetime.date.today()
            )
            dbsession.add(model)

    @classmethod
    def tear_down_db(cls):
        """Tear down database."""
        from portfolio.models.meta import Base
        Base.metadata.drop_all(bind=cls.engine)

    def test_home_page_200(self):
        """Test home get 200 code."""
        response = self.testapp.get('/')
        self.assertEqual(response.status_code, 200)

    def test_blog_posts_200(self):
        """Test blog get 200 code."""
        response = self.testapp.get('/blog')
        self.assertEqual(response.status_code, 200)

    def test_individual_blog_post_route(self):
        """Test individual blog post route 200 code."""
        response = self.testapp.get('/blog/1')
        self.assertEqual(response.status_code, 200)

    def test_api_blog_posts_200(self):
        """Test api posts route 200 code."""
        response = self.testapp.get('/api/posts')
        self.assertEqual(response.status_code, 200)

    def test_api_individual_blog_posts_200(self):
        """Test api post route 200 code."""
        response = self.testapp.get('/api/posts/1')
        self.assertEqual(response.status_code, 200)

    def test_login_200(self):
        """Test login route 200 code."""
        response = self.testapp.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_302(self):
        """Test logout routes 302 code."""
        response = self.testapp.get('/logout')
        self.assertEqual(response.status_code, 302)


class TestViewsFailureCondition(BaseTest):
    """Test Views Failure Condition."""

    pass

if __name__ == '__main__':
    unittest.main()
