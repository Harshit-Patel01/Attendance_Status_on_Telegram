import requests
import json
import math
import os
import schedule
import time
from datetime import datetime

LOGIN_URL = "https://kiet.cybervidya.net/api/auth/login"
COURSES_URL = "https://kiet.cybervidya.net/api/student/dashboard/registered-courses"

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Telegram bot details
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATE_FILE = "attendance_state.json"


def login():
    payload = {"userName": USERNAME, "password": PASSWORD}
    resp = requests.post(LOGIN_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()["data"]
    return data["auth_pref"], data["token"]


def fetch_courses(auth_pref, token):
    headers = {"Authorization": auth_pref + token}
    resp = requests.get(COURSES_URL, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    print("Telegram status:", r.json())


def calculate_attendance_message(course, present, total, status):
    percentage = (present / total * 100) if total > 0 else 0
    
    status_emoji = "✅" if status == "Present" else "❌"
    msg = f"📘 *{course}*\n{status_emoji} Marked as *{status}*\nAttendance: {present}/{total} ({percentage:.2f}%)"

    if percentage < 75:
        x = math.ceil((0.75 * total - present) / 0.25)
        if x < 0: 
            x = 0
        msg += f"\n⚠️ Below 75%! You must attend at least {x} more lecture(s) in a row."
    else:
        y = math.floor(present / 0.75 - total)
        if y < 0: 
            y = 0
        msg += f"\n✅ Safe! You can skip up to {y} lecture(s) while staying ≥75%."
    return msg


def check_attendance():
    print(f"Checking attendance at {datetime.now()}...")
    # Step 1: Login
    auth_pref, token = login()

    # Step 2: Fetch courses
    courses = fetch_courses(auth_pref, token)

    # Step 3: Load previous state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            prev_state = json.load(f)
    else:
        prev_state = {}

    new_state = {}

    # Step 4: Compare and send updates
    for c in courses:
        code = c["courseCode"]
        comp = c["studentCourseCompDetails"][0]
        present = comp["presentLecture"]
        total = comp["totalLecture"]

        new_state[code] = {"present": present, "total": total}

        old = prev_state.get(code, {})
        if old.get("present") != present or old.get("total") != total:
            # Determine status
            status = "Unknown"
            old_present = old.get("present", 0)
            old_total = old.get("total", 0)
            if present > old_present and total > old_total:
                status = "Present"
            elif present == old_present and total > old_total:
                status = "Absent"

            # Attendance changed → send Telegram message
            msg = calculate_attendance_message(c["courseName"], present, total, status)
            send_telegram(msg)

    # Step 5: Save new state
    with open(STATE_FILE, "w") as f:
        json.dump(new_state, f)


if __name__ == "__main__":
    check_attendance()