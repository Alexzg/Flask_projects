from flask import (
	Blueprint, render_template, g
)
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_registered_user():
    g.email = None # global variable

def registration_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.email is None:
            return render_template('error/error_404.html')
        return view(**kwargs)
    return wrapped_view