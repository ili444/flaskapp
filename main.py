from app import app
from view import *
from app import db
from books.blueprint import books
from authors.blueprint import authors


app.register_blueprint(books, url_prefix='/books')
app.register_blueprint(authors, url_prefix='/authors')

if __name__ == '__main__':
    app.run()