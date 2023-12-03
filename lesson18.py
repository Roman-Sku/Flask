from sqlalchemy import exc
from flask import Flask, Response, request
from crud import get_note, create_note
from models import create_tables

app = Flask(__name__)

create_tables()


@app.route('/', methods=['GET'])
def get_register_view():
    return (
        "<h1> Создание записи </h1>"
        '<form action="/" method="post">'
        '   <p> Заголовок: <input type="text" name="title"> </p>'
        '   <p> Содержимое: <input type="text" name="content"> </p>'
        '   <p> <input type="submit"> </p>'
    )


@app.route('/', methods=['POST'])
def register_note_view():
    note_data = request.form
    note = create_note(
        title=note_data["title"],
        content=note_data["content"]
    )
    return f"""
        <h1> Ваша запись была успешно создана </h1>
        <p> UUID: {note.uuid} </p>
    """


@app.route('/<note_uuid>', methods=['GET'])
def note_view(note_uuid: str):
    try:
        note = get_note(note_uuid)
    except exc.NoResultFound:
        return Response('Note not found', status=404)

    return f"""
        <h1> Вы зашли на запись {note.uuid} </h1>
        <p> Title: {note.title} </p>
        <p> Content: {note.content} </p>
        <p> Created at: {note.created_at} </p>
    """
