from flask import Flask, request, render_template
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets přístup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Otevři tabulku
sheet = client.open_by_key("1k9cWFABAQdQ9QdpjO_-tUVhrKLbrpNhCatZincGLu7o").sheet1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log_action():
    data = request.get_json()
    name = data.get("name", "neznámý")
    action = data.get("action", "neurčeno")
    timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    sheet.append_row([timestamp, name, action])
    return {"status": "ok"}
