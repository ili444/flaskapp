from app import db
from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin

def slugify(s):
    pattern = r'[^\w+]'
    return str(re.sub(pattern, '-', str(s)).lower())

book_aut = db.Table('book_aut',
                    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                    db.Column('author_id', db.Integer, db.ForeignKey('author.id')))


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(150), unique=True)
    annotation = db.Column(db.Text)
    year = db.Column(db.String(4))
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Books, self).__init__(*args, **kwargs)
        self.generate_slug()

    authors = db.relationship('Author', secondary=book_aut, backref=db.backref('books', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Book id: {self.id}, title: {self.title}>'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Author id: {self.id}, name: {self.name}>'


roles_users = db.Table('roles_users',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def __repr__(self):
        return f'< {self.email} >'

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'< {self.name} >'