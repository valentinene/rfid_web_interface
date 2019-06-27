from flask import (
    Blueprint, g, render_template
)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('pontaj', __name__)

@bp.route('/')
@login_required
def index():
	db=get_db()
	user = None
	pontaj = None
	if g.user is not None:
		user = g.user['username']
		id_tag = db.execute(
				"SELECT id_tag FROM angajati WHERE nume = ?", (str(user), )
		).fetchone()
		if id_tag is not None:
			pontaj = db.execute(
				"SELECT id_tag as id_card, id_camera as camera, DATETIME(timestamp,'localtime') as timp FROM pontaj WHERE id_tag = ? ", (str(id_tag['id_tag']), )
			).fetchall()
	if pontaj is not None:
		return render_template('pontaj/index.html', pontaje = pontaj)
	else:
		return render_template('pontaj/index.html')
