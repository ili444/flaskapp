from wtforms import Form, StringField, TextAreaField

class BookForm(Form):
    title = StringField('Title')
    annotation = TextAreaField('Annotation')