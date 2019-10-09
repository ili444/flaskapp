from flask import Blueprint
from flask import render_template

from models import Books, Author
from .forms import BookForm

from flask import request
from app import db

from flask import redirect
from flask import url_for

from flask_security import login_required

from view import Search

books = Blueprint('books', __name__, template_folder='templates')



@books.route('/')
@login_required
def list_book():
    result = Search(request, 'books/list_book.html')
    return result.run()

"""Обновление книги"""
@books.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_book(slug):
    """1.Исходя из slug get-запроса получаем экземпляр класса Books"""
    book = Books.query.filter(Books.slug==slug).first_or_404()

    """3. Юзер отправляет POST запрос с измененными данными, записываем в БД"""
    if request.method == 'POST':
        form = BookForm(formdata=request.form, obj=book)
        form.populate_obj(book)
        db.session.commit()

        return redirect(url_for('books.book_info', slug=book.slug))

    """2. Передаем экземпляр book в класс BookForm, рендерим шаблон, получаем форму с заполненными данными"""
    form = BookForm(obj=book)
    return render_template('books/book_edit.html', book=book, form=form)


"""Создание книги"""
@books.route('/create', methods=['POST', 'GET'])
@login_required
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        annotation = request.form['annotation']
        """Данные из POST запроса заносим в БД"""
        try:
            book = Books(title=title, annotation=annotation)
            db.session.add(book)
            db.session.commit()
        except:
            print('Error')
        """Перенаправляем на страницу со списком книг"""
        return  redirect(url_for('books.list_book'))
    """Иначе выгружаем форму для добавления книги"""
    form = BookForm()
    return render_template('books/create_book.html', form=form)


@books.route('/<slug>')
@login_required
def book_info(slug):
    """Исходя из slug get-запроса юзера выдаем страницу с информацией о книге"""
    book = Books.query.filter(Books.slug==slug).first_or_404()
    author = book.authors
    return render_template('books/book_info.html', book=book, author=author)
