from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post
import pdb

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('wrong'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        #create 4 users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='sharizan', email='sharizan@example.com')
        u3 = User(username='aygun', email='aygun@example.com')
        u4 = User(username='zu', email='zu@example.com')
        db.session.add_all([u1, u2, u3, u4])

        #create 4 posts
        now = datetime.utcnow()
        p1 = Post(author=u1, body="made by John", timestamp=now+timedelta(seconds=1))
        p2 = Post(author=u2, body="Sharizan feels good today", timestamp=now+timedelta(seconds=4))
        p3 = Post(author=u3, body="Aygun got a new job!", timestamp=now+timedelta(seconds=3))
        p4 = Post(author=u4, body='Just another post by Zu', timestamp=now+timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        #setup the followers
        u1.follow(u2) # John follows Sharizan
        u1.follow(u4) # John follows Zu
        u2.follow(u3) # Sharizan follows Aygun
        u3.follow(u4) # Aygun follow Zu
        db.session.commit()

        #check followed posts of each user
        #pdb.set_trace()
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__=='__main__':
    unittest.main(verbosity=2)

