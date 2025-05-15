import streamlit as st
import json
import os
import pandas as pd
from utils import login, get_groups, get_rooms, create_group

TOKEN_FILE = "token.json"

def save_token_user(resp_login):
    with open(TOKEN_FILE, "w") as f:
        json.dump(resp_login, f)

def load_token_user():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None

def delete_token_user():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

# Load session state if not present
if "token" not in st.session_state or "user" not in st.session_state:
    resp_login = load_token_user()
    if resp_login:
        st.session_state.token = resp_login.get("token")
        st.session_state.user = resp_login
    else:
        st.session_state.token = None
        st.session_state.user = None

st.title("Admin Maqdis Connect")

def do_login():
    email = st.session_state.email
    password = st.session_state.password
    try:
        resp = login(email, password)
        st.session_state.token = response.json().get("token")
        st.session_state.user = resp
        save_token_user(resp)
        st.success(f"Login berhasil. Selamat datang, {resp['username']}!")
        st.rerun()
    except Exception as e:
        st.error(f"Login gagal: {e}")

if st.session_state.token is None:
    st.subheader("Login")
    st.text_input("Email", key="email")
    st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=do_login)
else:
    user = st.session_state.user
    st.sidebar.write(f"👋 Selamat datang!")

    try:
        groups = get_groups(st.session_state.token)
        st.sidebar.write(f"📊 Grup tersedia: {len(groups)}")
    except Exception as e:
        st.error(f"Gagal memuat daftar grup: {e}")
        groups = []

    page = st.sidebar.selectbox("Navigasi Cepat", ["Lihat Grup", "Lihat Room", "Buat Grup Baru", "Logout"])

    if page == "Lihat Grup":
        st.header("Daftar Grup")
        if groups:
            data = [
                {
                    "Nama Grup": g['nama_grup'],
                    "created_at": g.get('created_at'),
                    "Kode Join": g.get('joinCode', ''),
                    "Room ID": g.get('roomid', '')
                }
                for g in groups
            ]
            df = pd.DataFrame(data)
            df['created_at'] = pd   .to_datetime(df['created_at'])
            df = df.sort_values('created_at')
            st.table(df.drop(columns=['created_at']))
        else:
            st.info("Belum ada grup yang tersedia.")


    elif page == "Lihat Room":
        st.header("Daftar Room")
        try:
            rooms_response = get_rooms(st.session_state.token)
            rooms = rooms_response.get("data", [])
            if rooms:
                for r in rooms:
                    st.write(f"- {r['nama_room']} (ID: {r['id']})")
            else:
                st.info("Belum ada room yang tersedia.")
        except Exception as e:
            st.error(f"Gagal memuat daftar room: {e}")


    elif page == "Buat Grup Baru":
        st.header("Buat Grup Baru")
        nama_grup = st.text_input("Nama Grup")
        if st.button("Buat Grup"):
            if nama_grup.strip() == "":
                st.error("Nama grup tidak boleh kosong.")
            else:
                try:
                    result = create_group(st.session_state.token, user["id"], nama_grup)
                    st.success(f"Grup '{result['group']['nama_grup']}' berhasil dibuat.")
                except Exception as e:
                    st.error(f"Gagal membuat grup: {e}")

    elif page == "Logout":
        st.session_state.token = None
        st.session_state.user = None
        delete_token_user()
        st.rerun()
