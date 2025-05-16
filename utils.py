import requests
import re
import time

API_BASE_URL = "https://jxjlm6b5-5000.asse.devtunnels.ms/"  

def login_user(email, password):
    try:
        res = requests.post(f"{API_BASE_URL}/api/auth/login", json={"email": email, "password": password})
        if res.status_code == 200:
            return res.json()
    except:
        return None

def get_groups(token):
    try:
        res = requests.get(f"{API_BASE_URL}/api/Group", headers={"token": token})
        return res.json()
    except:
        return []

def get_rooms(token):
    try:
        res = requests.get(f"{API_BASE_URL}/api/Audio/getRoom", headers={"token": token})
        return res.json()["getAllrooms"]
    except:
        return []

def get_profile(token):
    try:
        res = requests.get(f"{API_BASE_URL}/api/profile/me", headers={"token": token})
        return res.json().get("data", {})
    except:
        return {}



def create_group(nama_grup, user_id, token):
    try:
        res = requests.post(
            f"{API_BASE_URL}/api/Group/admin",
            json={"nama_grup": nama_grup},
            headers={"token": token}
        )
        return res.json()["data"]
    except:
        return {}

def generate_room(nama_room, token):
    try:
        res = requests.post(
            f"{API_BASE_URL}/api/Audio/generateToken",
            json={"nama_room": nama_room},
            headers={"token": token}
        )
        if res.status_code == 200:
            return res.json()["room"]
        else:
            print("Error creating room:", res.text)
            return None
    except Exception as e:
        print("Exception during room creation:", e)
        return None


def refresh_token(room_id, token):
    try:
        res = requests.post(
            f"{API_BASE_URL}/api/Audio/refreshToken",
            json={"room_Id": room_id},
            headers={"token": token}
        )
        if res.status_code == 200:
            return res.json()["room"]
        else:
            print("Error refreshing token:", res.text)
            return None
    except Exception as e:
        print("Exception during token refresh:", e)
        return None


def assign_room(room_id, grup_id, token):
    try:
        res = requests.post(
            f"{API_BASE_URL}/api/Audio/assignRoom",
            json={"roomid": room_id, "grupid": grup_id},
            headers={"token": token}
        )
        return res.json()
    except:
        return {}

def is_valid_email(email):
    return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email) is not None

def is_valid_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def is_valid_whatsapp(number):
    return re.fullmatch(r"\d{10,15}", number) is not None

def register_user(name, email, password, whatsapp):
    name = f"Admin {name.strip()}"
    payload = {
        "name": name,
        "email": email,
        "role": "admin",
        "password": password,
        "whatsapp": whatsapp
    }
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/register", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def request_otp(email):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/email/request-otp",
            json={"email": email, "type": "register"}
        )
        return response.json()
    except Exception as e:
        return {"message": f"Error: {e}"}

def verify_otp(email, otp):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/email/verify-otp",
            json={"email": email, "otp": otp}
        )
        return response.json()
    except Exception as e:
        return {"message": f"Error: {e}"}