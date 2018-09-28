from flask import (
	Blueprint, Flask, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('board', __name__)

@bp.route('/')
def index():
	db = get_db()
	entry = db.execute(
		'SELECT d.id, operator_id, title, content, created, username'
		' FROM userdata d JOIN user u ON d.operator_id=u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('board/index.html', entry=entry)
	
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		error = None
		
		if not title:
			error = 'Title is required!'
			
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO userdata (title, content, operator_id)'
				' VALUES (?, ?, ?)',
				(title, content, g.user['id'])
			)
			db.commit()
			return redirect(url_for('board.index'))
	return render_template('board/create.html')

def get_entry(id, check_operator=True):
	entry = get_db().execute(
		'SELECT d.id, operator_id, title, content, created, username'
		' FROM userdata d JOIN user u ON d.operator_id=u.id'
		' WHERE d.id = ?', (id,)
	).fetchone()
	
	if entry is None:
		abort(404, "Entry id:{0} is nowhere to be seen!".format(id))
	if check_operator and entry['operator_id']!=g.user['id']:
		abort(403)
	return entry
	
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
	entry = get_entry(id)
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		error = None
		
		if not title:
			error = 'Title is required!'
		
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE userdata SET title = ?, content = ?'
				' WHERE id = ?', (title, content, id)
			)
			db.commit()
			return redirect(url_for('board.index'))
	return render_template('board/update.html', entry=entry)
	
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_entry(id) # Check user & entry
	db = get_db()
	db.execute('DELETE FROM userdata WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('board.index'))