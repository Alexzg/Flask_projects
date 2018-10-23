from flask_mail import Mail, Message
from flask import current_app, render_template

def send_email(user_email, token):
	mail = Mail(current_app)
	try:
		msg = Message()
		msg.subject = 'Mietright Gmbh - online signature process'
		msg.sender = ''
		msg.recipients = [user_email]
		msg.body = 'Lorem ipsum....'
		msg.html = render_template('mail/message.html', token=token, user_email=user_email)
		mail.send(msg)
		print('mail sent')
		return render_template('mail/mail_sent.html')
	except Exception as e:
		print(str(e))
		return render_template('mail/mail_not_sent.html')