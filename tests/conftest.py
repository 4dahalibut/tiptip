# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import logging
import os
import tempfile

import pytest
from webtest import TestApp

import autoapp
from tiptip.app import create_app
from tiptip.database import db as _db
from .factories import AdminFactory, UserFactory


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory(password="myprecious")
    db.session.commit()
    return user


@pytest.fixture
def admin(db):
    """Create user for the tests."""
    user = AdminFactory(password="myprecious")
    db.session.commit()
    return user


# @pytest.fixture
# def client():
#     db_fd, autoapp.app.config['DATABASE'] = tempfile.mkstemp()
#     autoapp.app.config['TESTING'] = True
#
#     with autoapp.app.test_client() as client:
#         with autoapp.app.app_context():
#             autoapp.init_db()
#         yield client
#
#     os.close(db_fd)
#     os.unlink(autoapp.app.config['DATABASE'])
