import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from burgeramt.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		email = request.form['email']
		db = get_db()
		error = None

		if not email:
			error = 'email is required!'
		elif db.execute(
			'SELECT id FROM user WHERE email = ?', (email,)
		).fetchone() is not None:
			error = "User's email {} is already registered.".format(email)

		if error is None:
			db.execute(
				'INSERT INTO user (email) VALUES (?)',
				(email,)
			)
			db.commit()
			return render_template('signaturit/welcome.html')
			#return redirect(url_for('signaturit.welcome'))

		flash(error)

	return render_template('auth/register.html')