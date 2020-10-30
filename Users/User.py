from flask_restful import Resource
from flask import g, request, jsonify
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import config
from instance import messageResponse as res, master_query, misc


class User(Resource):
    def post(self):
        try:
            data = request.json
            email = data["email"]
            # name = data["username"]
            dt_string = misc.current_date()
            cur = g.appdb.cursor()
            user_query = master_query.user_query
            cur.execute(, (email, email, dt_string))
            g.appdb.commit()
            return jsonify({"status": "success", "response": res.mail_created})
        except Exception as error:
            return jsonify({"status": "Error", "Response": str(error)})


class DraftMail(Resource):
    def post(self):
        try:
            cur = g.appdb.cursor()
            data = request.json
            subject = data["subject"]
            body = data["body"]
            sender = data["sender"]
            recipients = data["recipients"]
            created_by = data["created_by"]
            draft_at = misc.current_date()
            draft_query = master_query.draft_query
            cur.execute(draft_query, (subject, body, sender, str(recipients), created_by, draft_at))
            g.appdb.commit()
            return jsonify({"status": "Success", "Response": res.success_draft})

        except Exception as error:
            return jsonify({"Status": "Failed", "Response": str(error)})


class SendMail(Resource):
    def post(self):
        try:
            cur = g.appdb.cursor()
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            data = request.json
            email_id = data['email_id']
            send_query = master_query.email_send_query
            cur.execute(send_query, (email_id))
            data = cur.fetchall()

            for reci in eval(data[0]['recipients']):
                sending_email = misc.send_email(data)
    
                try:
                    status_query = master_query.eamil_status_query
                    cur.execute(status_query, (email_id, reci, 'sent', sent_at))
                    g.appdb.commit()

                except :
                    status_query = master_query.pending_query
                    cur.execute(status_query, (email_id, reci, 'pending', sent_at))
                    g.appdb.commit()

            return jsonify({'status': 'Success', 'response': res.sent_success})

        except Exception as error:
            return jsonify({"Status": "Failed", "Response": str(error)})


class GetEmailList(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            user_id = request.args.get("user_id", False)
            if user_id:
                user_emails = "SELECT * FROM email WHERE created_by= %s" 
                cur.execute(user_emails, user_id)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class EmailStatus(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            eid = request.args.get("eid", False)
            eid_query = master_query.eid_query
            if eid:
                cur.execute(eid_query, eid)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class EmailDetails(Resource):
    def get(self):
        try:
            cur = g.appdb.cursor()
            eid = request.args.get("eid", False)
            eid_query = misc.user_id_query
            if eid:
                cur.execute(eid_query, eid)
                data = cur.fetchall()
                return jsonify({"status": "success", "Response": data})
        except Exception as error:
            return jsonify({"status": "Failed", "Response": str(error)})


class PendingMail(Resource):
    def get(self, action):
        cur = g.appdb.cursor()

        if action == "view":
            user_id = request.args.get("user_id", False)
            if user_id:
                view_query = master_query.pending_view_query
                cur.execute(view_query, user_id)
                data= cur.fetchall()
                return jsonify({"status": "success", "Response":data})
            else:
                return jsonify({"status": "Failed", "Response": res.userId_required})

        if action == "resend":
            email_id= request.args.get("email_id", False)
            if email_id:
                view_query = master_query.view_query
                cur.execute(view_query, email_id)
                data = cur.fetchall()
                if any(data):
                    misc.send_email(data)

                else:
                    return jsonify({"status": "Failed", "Response": res.no_pending})

                return jsonify({"status": "success","Response":data})
            else:
                return jsonify({"status": "Failed", "Response": res.required})
        else:
            return jsonify({"status": "Failed", "Response": res.invalid_param})

