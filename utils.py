import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def login(email: str, password: str):
    url = f"{BASE_URL}/api/auth/login"
    payload = {"email": email, "password": password}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

def get_groups(token: str):
    url = f"{BASE_URL}/api/Group"
    # Tidak butuh token
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

import requests

def get_rooms(token):
    url = f"{BASE_URL}/api/Audio/getRoom"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Biar error langsung dilempar kalau 4xx/5xx
    return response.json()


def create_group(token: str, user_id: str, nama_grup: str):
    headers = {"Authorization": f"Bearer {token}"}

    # 1. create group admin
    url_admin = f"{BASE_URL}/api/Group/admin?userId={user_id}"
    payload = {"nama_grup": nama_grup}
    r_admin = requests.post(url_admin, headers=headers, json=payload)
    r_admin.raise_for_status()
    group_data = r_admin.json().get("data")

    # 2. generate room token (butuh token)
    url_generate = f"{BASE_URL}/api/Audio/generateToken"
    room_payload = {"nama_room": nama_grup}
    r_generate = requests.post(url_generate, headers=headers, json=room_payload)  # tambahkan headers!
    r_generate.raise_for_status()
    room_data = r_generate.json().get("room")

    # 3. assign room to group
    url_assign = f"{BASE_URL}/api/Audio/assignRoom"
    assign_payload = {"roomid": room_data["id"], "grupid": group_data["grupid"]}
    r_assign = requests.post(url_assign, headers=headers, json=assign_payload)
    r_assign.raise_for_status()

    # 4. refresh token for room
    url_refresh = f"{BASE_URL}/api/Audio/refreshToken"
    refresh_payload = {"room_Id": room_data["id"]}
    r_refresh = requests.post(url_refresh, headers=headers, json=refresh_payload)
    r_refresh.raise_for_status()
    refreshed_room = r_refresh.json().get("room")

    return {
        "group": group_data,
        "room": refreshed_room
    }
