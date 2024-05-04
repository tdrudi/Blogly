from app import app
from models import db, Users, Posts
from unittest import TestCase

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

DEFAULT_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

class UserModelTestCase(TestCase):
    def setUp(self):
        """Clean up any existing users"""
        with app.app_context():
            Users.query.delete()
            user = Users(first_name='John', last_name='Doe', image_url=DEFAULT_URL)
            db.session.add(user)
            db.session.commit()

            self.user_id=user.id
        
    def tearDown(self):
        """Clean up db.session"""
        with app.app_context():
            db.session.rollback()

    def test_user_details(self):
        with app.app_context():
            with app.test_client() as client:
                """Test New User Form"""
                resp = client.get(f'/users/{self.user_id}')
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>John Doe</h1>', html)

    def test_new_user(self):
         with app.app_context():
            with app.test_client() as client:
                """Test New User Form"""
                data = {"first_name":"Jane", "last_name":"Doe", "image_url":DEFAULT_URL}
                resp = client.post('/users/new', data=data, follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('Jane Doe', html)

    def test_redirect(self):
        with app.test_client() as client:
            """Test - Redirect Homepage to ALl Users page"""
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)


class PostsModelTestCase(TestCase):
    def setUp(self):
        """Clean up any existing posts"""
        with app.app_context():
            Posts.query.delete()
            post = Posts(title='Test', post_content='This is a test.')
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id

    def tearDown(self):
        """Clean up db.session"""
        with app.app_context():
            db.session.rollback()

    def test_post_details(self):
        with app.app_context():
            with app.test_client() as client:
                """Test New User Form"""
                resp = client.get(f'/posts/{self.post_id}')
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>Test</h1>', html)
        