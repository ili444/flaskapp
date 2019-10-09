from app import app
from flask import render_template
from models import Books, Author

from flask import request
from flask_security import login_required


class Search:

    def __init__(self, request, template, read_page):
        self.request = request
        self.template = template
        self.read_page = read_page

    def run(self):
        q = request.args.get('q')

        page = request.args.get('page')

        if q:
            return self.search_run(q, page)

        books = Books.query.order_by(Books.date.desc())

        if self.read_page:
            books = Author.query.all()

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1



        pages = books.paginate(page=page, per_page=5)

        return render_template(self.template, pages=pages)

    def search_run(self, q, page):
        if q:
            """1. Ищем по названию книги"""
            books = Books.query.filter(Books.title.contains(q) | Books.annotation.contains(q))  # .all()
            """2. Ищем по автору"""
            try:
                authors = Author.query.filter(Author.name.contains(q)).first().books  # .all()
                """3. Объединяем два запроса"""
                books = books.union(authors)
            except:
                pass

            if books.all():
                pages = books.paginate(page=page, per_page=5)
                return render_template(self.template, books=books.all(), pages=pages)
            else:
                """Выгружает список книг сортируя по дате """
                books = Books.query.order_by(Books.date.desc())
                pages = books.paginate(page=page, per_page=5)
                return render_template(self.template, result_search='Поиск результатов не дал',
                                       books=books.all(), pages=pages)

@app.route('/')
@login_required
def index():
    result = Search(request, 'index.html')
    return result.run()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

"""Редактирование (доступно авторизованному пользователю при наличии аутентификации):
Управление списком книг: добавить / удалить / редактировать книгу.
Управление списком авторов: добавить / удалить / редактировать автора.
Запись о книге содержит следующие данные: ID, Название.
Запись об авторе содержит следующие данные: ID, Имя.

Связь между книгами и авторами – многие ко многим.

@Поиск книг по названию либо автору (доступно анонимному пользователю ).
Аутентификации и авторизация (по желанию кандидата)."""