from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from .keep import keep
from .label import is_public
import markdown

page = Blueprint("page", __name__)


@page.route("/note/<id>")
@login_required
def note(id):
    note = keep.get(id)
    if not note:
        abort(404, "note not found")
    if current_user.id != "admin" and not is_public(note):
        abort(403)
    content = []
    # TODO: move content creation into jinja
    if note.images:
        thumbnail = note.images[0].blob
        if thumbnail.height < thumbnail.width:
            content.append(f'<img src="/img/{ note.server_id }:0" /><br />')
    if note.title:
        content.append(f"<h1>{ note.title }</h1><br />")
    if note.text:
        content.append(markdown.markdown(note.text, extensions=["nl2br"]))

    return render_template("page.html", content="".join(content))
