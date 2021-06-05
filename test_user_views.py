import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="username", email = "email@email.com", password = "password", image_url=None)

        self.test_id = 1357

        self.testuser.id = self.test_id

        self.u1 = User.signup("abc", "test1@test.com", "password", None)
        self.u1_id = 778
        self.u1.id = self.u1_id

        self.u2 = User.signup("usertwo", "test2@test.com", "password", None)
        self.u2_id = 800
        self.u2.id = self.u2_id

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users(self):
        with self.client as c:
            resp = c.get('/users')

            self.assertEqual(resp.status_code, 200)

    def test_users_following(self):
        with self.client as c:
            resp = c.get('/users/1357/following')

            self.assertEqual(resp.status_code, 302)

    def test_users_followers(self):
        with self.client as c:
            resp = c.get('/users/1357/followers')

            self.assertEqual(resp.status_code, 302)

    def test_new_message(self):
        m = Message(id=1984, text="new message", user_id=self.u1_id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/messages/new", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)



