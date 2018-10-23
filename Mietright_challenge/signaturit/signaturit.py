from flask import (
	Blueprint, flash, redirect, request, render_template, url_for, g
)
import jwt, functools

bp = Blueprint('signaturit', __name__, url_prefix='/signaturit')

from instance.signaturit_config import TOKEN_KEY
from signaturit.auth import registration_required

# the Main page sends here after registration
@bp.route('/<token>/mail', methods=['GET'])
def mail(token):
	from signaturit.mail import send_email
	
	""" (example) 
	email = 'user@dmndmn.com'
	encoded_token = jwt.encode({'email': email}, TOKEN_KEY, algorithm='HS256')
	"""
	"""
	encoded_token for test is <- eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJAZG1uZG1uLmNvbSJ9.19AapUepRB9q61XuRhDN9WoYbE32JDzA4lSnuU2v_AA
	"""
	try: # Decode token and procceed
		decoded_token = jwt.decode(token, TOKEN_KEY, algorithm='HS256')
	except: # If problem, render error page
		return render_template('error/error_404.html')
		
	return send_email(user_email=decoded_token['email'], token=token)
	
@bp.route('/<token>/form', methods=['GET', 'POST'])
def form(token):
	try:
		decoded_token = jwt.decode(token, TOKEN_KEY, algorithm='HS256')
	except: 
		return render_template('error/error_404.html')
		
	if request.method == 'POST':
		signed_paper = request.form['signed_doc_img']
		error = None
		if signed_paper is not None:
			return "Success - End of challenge"
		
	return render_template('form/main_form.html')
	