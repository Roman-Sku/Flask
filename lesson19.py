from sqlalchemy import exc
from flask import Flask, Response, request, render_template, redirect, url_for
from crud import get_note, create_note, get_all_notes
from models import create_tables

app = Flask(__name__,
            template_folder="templates",
            static_folder="static",
            static_url_path="/static-files/"
            )

create_tables()


@app.route('/create', methods=['GET'])
def get_register_view():
    return render_template("create_note_form.html")


@app.route('/create', methods=['POST'])
def register_note_view():
    note_data = request.form
    note = create_note(
        title=note_data["title"],
        content=note_data["content"]
    )
    return redirect(url_for("note_view", note_uuid=note.uuid))


@app.route('/<note_uuid>', methods=['GET'])
def note_view(note_uuid: str):
    try:
        note = get_note(note_uuid)
    except exc.NoResultFound:
        return Response('Note not found', status=404)

    return render_template('note.html',
                           uuid=note.uuid,
                           title=note.title,
                           time=note.created_at,
                           content=note.content)


@app.route('/', methods=['GET'])
def home_page():
    all_notes = get_all_notes()
    return render_template("home_page.html", notes=all_notes)
