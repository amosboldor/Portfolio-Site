"""Testing File."""
import datetime
import unittest
import json
import re
import transaction
from portfolio.models import get_tm_session, BlogPost
from portfolio.models.meta import Base
from portfolio import main
from pyramid import testing
from webtest import TestApp
from bs4 import BeautifulSoup


def dummy_request(dbsession):
    """Return Dummy Request."""
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    """Base Test with db setup."""

    @classmethod
    def setUp(cls):
        """Add to database."""
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


class TestViewsSuccessCondition(BaseTest):
    """Test Views Success Condition."""

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

    def test_project_200(self):
        """Test project route 200 code."""
        response = self.testapp.get('/projects')
        self.assertEqual(response.status_code, 200)

    def test_individual_blog_post_route_shows_post(self):
        """Test individual blog post route shows post."""
        response = self.testapp.get('/blog/1')
        self.assertTrue("Test Title" in response)
        self.assertTrue("Test Body" in response)
        self.assertTrue(str(datetime.date.today()) in response)

    def test_api_individual_blog_posts_200_is_correct_post(self):
        """Test api post route 200 code is correct post."""
        response = self.testapp.get('/api/posts/1')
        post_json = response.json
        post_in_db = {
            'date': str(datetime.date.today()),
            'title': 'Test Title',
            'body': 'Test Body',
            'html': '<p>Test Body</p>'
        }
        self.assertEqual(post_json, post_in_db)

    def test_delete_post(self):
        """Test delete post deletes post."""
        response = self.testapp.get('/blog')
        self.assertTrue("Test Title" in response)
        self.assertTrue("Test Body" in response)
        self.assertTrue(str(datetime.date.today()) in response)

        self.testapp.post('/login', params={'Username': 'amos', 'Password': 'password'})
        script_tag = self.testapp.get('/blog').html.find_all("script")[4].string
        csrfToken = re.findall('var csrfToken = (.*?);\s*$', script_tag, re.M)[0][1:-1]
        self.testapp.delete('/blog/1/delete', headers={'X-CSRF-Token': csrfToken})

        response = self.testapp.get('/blog')
        self.assertFalse("Test Title" in response)
        self.assertFalse("Test Body" in response)
        self.assertFalse(str(datetime.date.today()) in response)


class TestViewsFailureCondition(BaseTest):
    """Test Views Failure Condition."""

    def test_individual_blog_post_route_404_wrong_id(self):
        """Test individual blog post route 404 code wrong id."""
        response = self.testapp.get('/blog/2', status=404)
        self.assertEqual(response.status_code, 404)

    def test_api_individual_blog_posts_404_wrong_id(self):
        """Test api post route 404 code wrong id."""
        response = self.testapp.get('/api/posts/2', status=404)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
