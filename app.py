"""
app.py — Women Safety Analytics
Flask backend — production-ready for Render deployment.
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import base64, os, numpy as np, cv2
from deepface import DeepFace
from twilio.rest import Client
from datetime import datetime
from database import save_report, get_recent_reports

load_dotenv()

app = Flask(__name__)

# ── CORS — allow all origins (needed for Render) ──
CORS(app, resources={r"/*": {"origins": "*"}})

# ── TWILIO CONFIG ─────────────────────────────────
TWILIO_SID    = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN",  "")
TWILIO_FROM   = os.getenv("TWILIO_FROM_NUMBER", "")
EMERGENCY_NUM = os.getenv("EMERGENCY_CONTACT",  "")
PORT          = int(os.getenv("PORT", 5500))  # Render sets PORT automatically

# ── HELPERS ──────────────────────────────────────
def b64_to_frame(b64_str):
    if "," in b64_str:
        b64_str = b64_str.split(",")[1]
    img_bytes = base64.b64decode(b64_str)
    np_arr    = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def get_threat_level(male_count):
    if male_count >= 3: return "High"
    if male_count >= 1: return "Moderate"
    return "Low"

# ── ROUTES ───────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

# ── KEEP ALIVE PING (for UptimeRobot) ────────────
@app.route("/ping")
def ping():
    return jsonify({"status": "alive", "time": datetime.now().isoformat()})

# ── GENDER + EMOTION DETECTION ───────────────────
@app.route("/detect", methods=["POST"])
def detect():
    try:
        data  = request.get_json(force=True)
        frame = b64_to_frame(data.get("image", ""))
        results = DeepFace.analyze(
            frame,
            actions=["gender", "emotion", "age"],
            enforce_detection=False,
            silent=True
        )
        if not isinstance(results, list):
            results = [results]
        people = []
        for r in results:
            gd  = r.get("gender", {})
            conf = round(max(gd.values()) if gd else 0, 1)
            people.append({
                "gender":     r.get("dominant_gender", "Unknown"),
                "emotion":    r.get("dominant_emotion", "Unknown"),
                "age":        int(r.get("age", 0)),
                "confidence": conf,
            })
        male_count   = sum(1 for p in people if p["gender"] == "Man")
        female_count = len(people) - male_count
        return jsonify({
            "success":      True,
            "people":       people,
            "total":        len(people),
            "male_count":   male_count,
            "female_count": female_count,
            "threat_level": get_threat_level(male_count),
            "timestamp":    datetime.now().strftime("%H:%M:%S"),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── SOS ALERT ────────────────────────────────────
@app.route("/sos", methods=["POST"])
def sos():
    try:
        data      = request.get_json(force=True)
        lat       = data.get("lat", "Unknown")
        lng       = data.get("lng", "Unknown")
        user_name = data.get("name", "User")
        contact   = data.get("contact", EMERGENCY_NUM)
        maps_link = f"https://maps.google.com/?q={lat},{lng}"
        timestamp = datetime.now().strftime("%d %b %Y, %H:%M IST")
        sms_body  = (
            f"🚨 EMERGENCY ALERT 🚨\n"
            f"{user_name} needs immediate help!\n\n"
            f"📍 Location: {lat}°N, {lng}°E\n"
            f"🗺 Maps: {maps_link}\n"
            f"⏰ Time: {timestamp}\n\n"
            f"Please respond immediately!"
        )
        if not TWILIO_SID or TWILIO_SID == "YOUR_TWILIO_ACCOUNT_SID":
            return jsonify({"success": False, "error": "Twilio credentials not configured."}), 400
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg    = client.messages.create(body=sms_body, from_=TWILIO_FROM, to=contact)
        return jsonify({"success": True, "message_sid": msg.sid, "sent_to": contact, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── INCIDENT REPORT ──────────────────────────────
@app.route("/report", methods=["POST"])
def report():
    try:
        data      = request.get_json(force=True)
        report_id = save_report(
            report_type = data.get("type",        "Other"),
            location    = data.get("location",    "Unknown"),
            description = data.get("description", ""),
            lat         = data.get("lat",         0),
            lng         = data.get("lng",         0),
            anonymous   = data.get("anonymous",   True),
        )
        return jsonify({"success": True, "report_id": report_id, "message": "Report submitted."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── GET REPORTS ──────────────────────────────────
@app.route("/reports", methods=["GET"])
def get_reports():
    try:
        return jsonify({"success": True, "reports": get_recent_reports(20)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── HEALTH CHECK ─────────────────────────────────
@app.route("/health")
def health():
    return jsonify({
        "status":  "running",
        "twilio":  bool(TWILIO_SID and TWILIO_SID != "YOUR_TWILIO_ACCOUNT_SID"),
        "time":    datetime.now().isoformat(),
    })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
