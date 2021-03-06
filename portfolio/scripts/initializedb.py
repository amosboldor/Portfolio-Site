"""Script that initializes the database."""
import datetime
import os
import sys

import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars

from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    BlogPost
)
from ..models.meta import Base


def usage(argv):
    """Error print function."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """Main db creation function."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    sql_url = os.environ.get('DATABASE_URL', 'sqlite:///BlogPostDB.sqlite')
    settings["sqlalchemy.url"] = sql_url

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        model = BlogPost(
            title='Test Title',
            body='Test Body',
            html='<p>Test Body</p>',
            date=datetime.date.today()
        )
        dbsession.add(model)
