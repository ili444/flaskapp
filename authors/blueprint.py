from flask import Blueprint
from flask import render_template

from flask import request

from models import Author
from .forms import AuthorForm
from flask_security import login_required

from view import Search

authors = Blueprint('authors', __name__, template_folder='templates')


@authors.route('/')
@login_required
def list_authors():
    result = Search(request, 'books/list_book.html')
    return result.run()


@authors.route('/<slug>')
@login_required
def author_info(slug):
    author = Author.query.filter(Author.slug==slug).first_or_404()
    books = author.books.all()
    return render_template('authors/author_info.html', author=author, books=books)
