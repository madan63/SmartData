#query is used to insert the values into user table
user_query = "insert into user(user_name, password, created_at) value(%s, %s, %s)"

draft_query = """insert into email(subject, body, sender, recipients, created_by, created_at) values(%s, %s, %s, %s, %s, %s)"""

email_send_query = """SELECT u.mailid, e.subject, e.body, e.sender, e.recipients FROM email e INNER JOIN USER u ON u.id= e.created_by WHERE eid= %s"""

email_status_query = """insert into email_status(email_id, recipient, status, sent_at) values(%s, %s, %s, %s)"""

status_update_query = """UPDATE email_status SET STATUS = 'sent' WHERE email_id = %s;"""

pending_query ="""insert into email_status(email_id,recipient,status, sent_at) values(%s, %s, %s, %s)"""

view_query = """SELECT e.subject, e.body, e.sender, es.status, es.recipient, e.recipients FROM email e 
INNER JOIN email_status es ON e.eid=es.email_id WHERE e.eid = %s AND es.status='pending'"""

pending_view_query = """SELECT e.subject,e.body,e.sender,es.status,es.recipient FROM email e 
INNER JOIN email_status es ON e.eid=es.email_id WHERE e.created_by = %s AND es.status='pending'"""

eid_query = """SELECT e.subject, e.body, e.sender, e.created_at, es.recipient, es.status, es.sent_at 
FROM email e INNER JOIN email_status es ON e.eid = es.email_id WHERE e.eid=%s"""

user_id_query = """SELECT u.username, u.mailid, e.subject, e.body, e.sender, e.recipients, e.created_at 
FROM USER u INNER JOIN email e ON u.id = e.created_by WHERE e.eid=%s"""
