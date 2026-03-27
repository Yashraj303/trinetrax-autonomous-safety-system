import os
import requests
from core.logic import *

# =========================
# SERVICE STATUS FILE
# =========================
STATUS_FILE = "service_status.txt"

# 👉 Paste your API key here (or leave as is for fallback)
API_KEY = "YOUR_API_KEY_HERE"


# =========================
# SERVICE CENTER FETCH (API + FALLBACK)
# =========================
def get_service_centers():
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": "18.5204,73.8567",  # Pune default
        "radius": 5000,
        "type": "car_repair",
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=3)
        data = response.json()

        if data.get("status") == "OK":
            centers = []

            for place in data["results"][:3]:
                name = place.get("name", "Service Center")

                maps_link = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}"

                centers.append({
                    "name": name,
                    "distance": "Nearby",
                    "maps_link": maps_link
                })

            return centers

        else:
            raise Exception("API failed")

    except Exception as e:
        print("⚠️ API FAILED → USING FALLBACK:", e)

        # 🔥 FALLBACK (always works)
        return [
            {
                "name": "Maruti Suzuki Service Center",
                "distance": "2 km",
                "maps_link": "https://www.google.com/maps/search/?api=1&query=Maruti+Suzuki+Service+Center+Pune"
            },
            {
                "name": "Tata Motors Service Center",
                "distance": "3 km",
                "maps_link": "https://www.google.com/maps/search/?api=1&query=Tata+Motors+Service+Center+Pune"
            },
            {
                "name": "Mahindra Service Center",
                "distance": "4 km",
                "maps_link": "https://www.google.com/maps/search/?api=1&query=Mahindra+Service+Center+Pune"
            }
        ]


# =========================
# SERVICE BOOKING CONTROL
# =========================
def is_service_booked():
    if not os.path.exists(STATUS_FILE):
        return False

    with open(STATUS_FILE, "r") as f:
        return f.read().strip() == "booked"


def set_service_booked():
    with open(STATUS_FILE, "w") as f:
        f.write("booked")


def reset_service_status():
    with open(STATUS_FILE, "w") as f:
        f.write("not_booked")


# =========================
# DATA AGENT
# =========================
def data_agent(initial, current, distance, braking):
    return {
        "initial": initial,
        "current": current,
        "distance": distance,
        "braking_events": braking
    }


# =========================
# DIAGNOSIS AGENT
# =========================
def diagnosis_agent(data):

    health = calculate_health(data["initial"], data["current"])
    wear = calculate_wear_rate(data["initial"], data["current"], data["distance"])
    rul = calculate_rul(data["current"], wear)

    factor = behavior_factor_v2(data["braking_events"], data["distance"])
    smart = smart_health_v2(health, factor, wear)

    style = detect_driving_style(data["braking_events"], data["distance"])
    trend = detect_trend(wear)

    usage = brake_usage(data["braking_events"], data["distance"])
    env = environment_factor("pune")
    pattern = usage_pattern(data["braking_events"], data["distance"])

    failure = failure_probability(smart)

    confidence = ai_confidence_v2(
        smart,
        wear,
        data["braking_events"],
        data["distance"]
    )

    return smart, wear, rul, style, trend, usage, env, pattern, failure, confidence


# =========================
# DECISION AGENT
# =========================
def decision_agent(health, rul):
    return classify_risk(health, rul)