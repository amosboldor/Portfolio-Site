"""Testing File."""
import unittest
import transaction
import datetime
from portfolio.models.meta import Base
from pyramid import testing


def dummy_request(dbsession):
    """Dummy Request."""
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    """Base Test."""

    def setUp(self):
        """Test setup."""
        from webtest import TestApp
        from portfolio import main

        app = main({}, **{'sqlalchemy.url': 'sqlite:///:memory:'})
        self.testapp = TestApp(app)

        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('portfolio.models')
        settings = self.config.get_settings()

        from portfolio.models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        """Initilize db."""
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        """Teardown db."""
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestViewsSuccessCondition(BaseTest):
    """Test Views Success Condition."""

    def setUp(self):
        """Setup."""
        super(TestViewsSuccessCondition, self).setUp()
        self.init_database()

        from portfolio.models import BlogPost
        model = BlogPost(
            title='Test Title',
            body='Test Body',
            date=datetime.date.today()
        )
        self.session.add(model)

    def test_home_page_200(self):
        """Test home get 200 code."""
        response = self.testapp.get('/')
        self.assertEquals(response.status_code, 200)


class TestViewsFailureCondition(BaseTest):
    """Test Views Failure Condition."""

    pass

if __name__ == '__main__':
    unittest.main()
