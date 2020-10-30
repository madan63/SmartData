from flask import g
from datetime import datetime as DT

def current_date():
	now = DT.now()
	dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
	return dt_string


def send_email(data):
	
	subject = data[0]['subject']
	sender = data[0]['sender']
	body = data[0]['body']
	sent_at = current_date()
	try:
		smtpserver = g.config.get("smtpserver")
		smtpport = g.config.get("smtpport")
		receipient = reci
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = sender
		msg['To'] = reci
		text = body
		part = MIMEText(text, 'plain')
		msg.attach(part)
		mail = smtplib.SMTP(smtpserver, smtpport)
		mail.ehlo()
		mail.starttls()
		mail.login(g.config.get("email"), g.config.get("smtppass"))
		mail.sendmail(g.config.get("email"), reci, msg.as_string())
		mail.quit()
	
	except smtplib.SMTPException as e:
		return jsonify({"status": "Failed", "Response": str(e)})
return True
