# Women Safety Analytics — Rakshak 🛡️
### Protecting Women from Safety Threats

**Amity University Uttar Pradesh**
Amity School of Engineering and Technology — Department of Information Technology
Integrated Project | Semester 5 | B.Tech IT (2023–27)

---

## Live Demo

🌐 **Deployed on Render:** `https://women-safety-analytics.onrender.com`

> **Note:** Free tier may take 30–50 seconds to wake up on first visit if inactive.
> UptimeRobot pings `/ping` every 5 minutes to keep it alive.

---

## Complete File Structure

```
women-safety/
├── app.py                  ← Flask backend (all 6 API routes)
├── database.py             ← Saves incident reports to reports.json
├── requirements.txt        ← Python dependencies for pip install
├── render.yaml             ← Render deployment configuration
├── runtime.txt             ← Specifies Python 3.11.0 for Render
├── .env                    ← Twilio credentials (never push to GitHub)
├── .gitignore              ← Prevents .env and venv from being pushed
├── run.bat                 ← Windows: double-click to run locally
├── run.sh                  ← Mac/Linux: bash run.sh to run locally
├── README.md               ← This file
└── templates/
    └── index.html          ← Complete 10-screen frontend webapp
```

---

## All 10 Features

| # | Feature | Technology | Status |
|---|---------|-----------|--------|
| 1 | Real-Time Dashboard | Custom charts + live feed | ✅ Complete |
| 2 | Gender Detection AI | DeepFace + OpenCV + Webcam | ✅ Complete |
| 3 | Live Location Map | Leaflet.js + Browser GPS | ✅ Complete |
| 4 | SOS Emergency Alert | Twilio SMS API | ✅ Complete |
| 5 | Danger Zone Heatmap | Leaflet.js circle overlays | ✅ Complete |
| 6 | Safe Route Planner | Leaflet.js polylines + scoring | ✅ Complete |
| 7 | Analytics Dashboard | Hourly charts + incident stats | ✅ Complete |
| 8 | Emotion Detection AI | DeepFace (same webcam) | ✅ Complete |
| 9 | Community Safety Feed | Real-time post and read | ✅ Complete |
| 10 | Incident Reporting | Saves to reports.json via database.py | ✅ Complete |

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Gender & Emotion AI | DeepFace 0.0.93 (Python) | Free |
| Webcam capture | OpenCV (opencv-python-headless) | Free |
| Deep Learning | TensorFlow 2.15.1 + tf-keras 2.15.1 | Free |
| Interactive Map | Leaflet.js 1.9.4 + OpenStreetMap | Free |
| GPS Location | Browser Geolocation API (W3C) | Free |
| SOS SMS | Twilio REST API | Free trial ($15.50) |
| Backend | Flask + Gunicorn (Python) | Free |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript | Free |
| Database | JSON file-based storage (database.py) | Free |
| Hosting | Render.com free tier | Free |
| Keep-alive | UptimeRobot (pings /ping every 5 min) | Free |

---

## Local Setup Instructions

### Prerequisites
- Python 3.11 installed
- Internet connection (for map tiles and DeepFace model download)
- A webcam (for gender and emotion detection)

---

### Step 1 — Clone or extract the project

```bash
cd C:\Users\YourName\Desktop
# Extract the ZIP or clone from GitHub
git clone https://github.com/Mahesh127f/Woman-Safety-Analytics_Rakshak.git
cd Woman-Safety-Analytics_Rakshak
```

---

### Step 2 — Install dependencies

**Windows (one click):**
```
Double-click run.bat
```

**Mac / Linux:**
```bash
bash run.sh
```

**Or manually in terminal:**
```bash
pip install -r requirements.txt
```

> First install takes 5–10 minutes — DeepFace and TensorFlow are large packages.

---

### Step 3 — Configure Twilio for SOS SMS (optional)

> Skip this step if you only want to test the other 9 features.
> The app works perfectly without Twilio — only the SMS sending won't work.

1. Sign up FREE at https://www.twilio.com (no credit card needed — $15.50 trial credit)
2. From your Twilio Console homepage, copy:
   - Account SID
   - Auth Token
3. Go to Phone Numbers → Active Numbers → copy your Twilio number
4. Go to Phone Numbers → Verified Caller IDs → add your mobile number
5. Open `.env` and fill in:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_NUMBER=+1415XXXXXXX
EMERGENCY_CONTACT=+919876543210
```

---

### Step 4 — Run the app

```bash
python app.py
```

You will see:
```
==================================================
  Women Safety Analytics — Backend
  http://127.0.0.1:5500
  Twilio configured: True
==================================================
* Running on http://127.0.0.1:5500
```

---

### Step 5 — Open in browser

```
http://127.0.0.1:5500
```

Click **Allow** when the browser asks for Camera and Location permissions.

---

## Deployment on Render

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/women-safety-analytics.git
git push -u origin main
```

### Step 2 — Deploy on Render

1. Go to https://render.com → Sign up with GitHub
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Set these values:

| Field | Value |
|---|---|
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --workers 1 --timeout 120 --bind 0.0.0.0:$PORT` |
| Instance Type | Free |

5. Add Environment Variables:

| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.11.0` |
| `TWILIO_ACCOUNT_SID` | Your SID (optional) |
| `TWILIO_AUTH_TOKEN` | Your token (optional) |
| `TWILIO_FROM_NUMBER` | Your Twilio number (optional) |
| `EMERGENCY_CONTACT` | +91XXXXXXXXXX (optional) |

6. Click **Create Web Service** — first deploy takes 10–15 minutes.

### Step 3 — Keep alive with UptimeRobot (prevents sleep)

1. Go to https://uptimerobot.com → Sign up free
2. Click **Add New Monitor**
3. Set:
   - Monitor Type: `HTTP(s)`
   - URL: `https://your-app-name.onrender.com/ping`
   - Interval: Every 5 minutes
4. Click **Create Monitor**

Your app will now stay awake 24/7 and open instantly every time.

---

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Serve the main webapp (index.html) |
| `/ping` | GET | Keep-alive endpoint for UptimeRobot |
| `/detect` | POST | DeepFace gender + emotion + age detection |
| `/sos` | POST | Send Twilio SOS SMS with GPS coordinates |
| `/report` | POST | Save incident report to reports.json |
| `/reports` | GET | Fetch 20 most recent incident reports |
| `/health` | GET | Check backend status and Twilio config |

---

## Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| `ModuleNotFoundError: deepface` | Run `pip install deepface==0.0.93` |
| Camera not working | Click Allow in browser — check browser permissions |
| GPS not working | Click Allow in browser — check browser permissions |
| SOS: Twilio not configured | Fill in `.env` with your Twilio credentials |
| SOS: not a verified number | Add number in Twilio Console → Verified Caller IDs |
| Port already in use | Change `FLASK_PORT=5501` in `.env` |
| `python` not recognized | Reinstall Python 3.11 with "Add to PATH" ticked |
| Render build failed | Check `PYTHON_VERSION=3.11.0` is set in Render environment variables |
| App slow to open on Render | Set up UptimeRobot to ping `/ping` every 5 minutes |

---

## How It Works

```
User opens browser
      ↓
Flask serves index.html (all 10 screens)
      ↓
Browser asks for Camera + GPS permission
      ↓
┌─────────────────────────────────────────┐
│  Camera feed → /detect → DeepFace AI   │
│  Returns: gender, emotion, threat level │
└─────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────┐
│  GPS coords → Leaflet.js map display   │
│  Danger zones shown as colour circles  │
└─────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────┐
│  SOS button → /sos → Twilio SMS API    │
│  Sends GPS + Maps link to contacts     │
└─────────────────────────────────────────┘
      ↓
┌─────────────────────────────────────────┐
│  Reports → /report → database.py       │
│  Saves to reports.json anonymously     │
└─────────────────────────────────────────┘
```

---

## Project Report Reference

- **Title:** Women Safety Analytics — Protecting Women from Safety Threats
- **Type:** Integrated Project, Semester 5
- **Abstract:** AI-powered emergency response system using DeepFace facial analysis, browser-based GPS geolocation, and Twilio SMS API
- **Key Modules:** Gender Detection, Emotion Detection, Location Tracking, SOS Alert, Heatmap, Safe Route, Analytics, Community Feed, Incident Reporting
- **Methodology:** Requirements Analysis → System Design → AI Module Development → Location Module → SOS Integration → Testing
