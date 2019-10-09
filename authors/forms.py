from wtforms import Form, StringField, TextAreaField

class AuthorForm(Form):
    name = StringField('Name')