import streamlit as st
import requests
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from utils import (
    login_user, get_groups, get_rooms, get_profile,
    create_group, generate_room, refresh_token, assign_room,
    register_user, request_otp, verify_otp  
)
from datetime import datetime

API_BASE_URL = "https://jxjlm6b5-5000.asse.devtunnels.ms" 
st.set_page_config(
    page_title="Maqdis Connect", 
    page_icon="./public/favicon.png",                      
    layout="wide"                       
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lusitana&family=Montserrat&display=swap');

    /* Atur font default seluruh aplikasi ke Montserrat */
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Lusitana', serif;
    }
    </style>
""", unsafe_allow_html=True)


# Inisialisasi session_state
if 'page' not in st.session_state:
    st.session_state.page = 'auth'
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = {}


with st.sidebar:
    selected = option_menu(
        menu_title="Maqdis",
        options=["Login", "Registration", "Dashboard", "Profile", "Group", "Room", "Manage"],
        icons=["box-arrow-in-right", "person-plus", "speedometer", "person-circle", "people", "house", "gear"],
        menu_icon="airplane", 
        default_index=2,
        orientation="vertical"
    )

# Simpan ke session_state (opsional)
st.session_state.page = selected.lower()

# Signin
if st.session_state.page == "login":
    if st.session_state.token:
        username = st.session_state.user.get("username", "Pengguna")
        st.info(f"Anda sudah login sebagai **{username}**.")
    else:
        st.title("📝 Log-in")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.token = user["token"]
                st.session_state.user = user
                st.success("Login berhasil!")
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Gagal login!")

# Signup
elif st.session_state.page == "registration":
    import time
    from utils import (
        is_valid_email,
        is_valid_password,
        is_valid_whatsapp,
        register_user,
        request_otp,
        verify_otp
    )

    

    if "pending_signup" not in st.session_state:
        st.session_state.pending_signup = {}
    if "otp_sent_time" not in st.session_state:
        st.session_state.otp_sent_time = None
    if "otp_ready" not in st.session_state:
        st.session_state.otp_ready = False

    if st.session_state.get("user"):
        username = st.session_state.user.get("username", "Pengguna")
        st.info(f"Anda sudah login sebagai **{username}**.")
    else:
        st.title("📝 Registration")
        with st.form("signup_form"):
            name = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            whatsapp = st.text_input("WhatsApp")
            submitted = st.form_submit_button("Daftar")

            if submitted:
                if not name:
                    st.error("Nama tidak boleh kosong!")
                elif not is_valid_email(email):
                    st.error("Format email tidak valid!")
                elif not is_valid_password(password):
                    st.error("Password harus lebih dari 8 karakter dan mengandung huruf besar, kecil, angka, dan simbol!")
                elif not is_valid_whatsapp(whatsapp):
                    st.error("Nomor WhatsApp harus 10-15 digit dan hanya angka!")
                else:
                    with st.spinner("Mendaftarkan akun dan mengirim OTP..."):
                        result = register_user(name, email, password, whatsapp)
                        if result.get("status") == "success":
                            st.success(result.get("message", "Pendaftaran berhasil."))

                            st.session_state.pending_signup = {
                                "name": name,
                                "email": email,
                                "password": password,
                                "whatsapp": whatsapp
                            }

                            otp_result = request_otp(email)
                            if otp_result.get("message") == "OTP dikirim":
                                st.success("OTP telah dikirim ke email Anda.")
                                st.session_state.otp_sent_time = time.time()
                                st.session_state.otp_ready = True
                            else:
                                st.error(otp_result.get("message", "Gagal mengirim OTP."))
                        else:
                            st.error(result.get("message", "Pendaftaran gagal."))

        if st.session_state.otp_ready:
            st.markdown("Masukkan kode OTP yang dikirim ke email Anda.")
            otp = st.text_input("Kode OTP", max_chars=4)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Verifikasi Akun Baru"):
                    with st.spinner("Memverifikasi OTP..."):
                        email = st.session_state.pending_signup.get("email")
                        result = verify_otp(email, otp)
                        if result.get("message") == "OTP valid":
                            st.success("✅ Akun berhasil diverifikasi. Silakan login.")
                            st.session_state.otp_ready = False
                            st.session_state.pending_signup = {}
                        else:
                            st.error(result.get("message", "OTP salah atau kadaluarsa."))

            with col2:
                can_resend = time.time() - st.session_state.otp_sent_time >= 10
                if st.button("Kirim Ulang OTP", disabled=not can_resend):
                    email = st.session_state.pending_signup.get("email")
                    result = request_otp(email)
                    if result.get("message") == "OTP dikirim":
                        st.success("OTP baru telah dikirim.")
                        st.session_state.otp_sent_time = time.time()
                    else:
                        st.error(result.get("message", "Gagal mengirim ulang OTP."))


# Dashboard
elif st.session_state.page == "dashboard":
    st.title("📊 Dashboard")
    if not st.session_state.token:
        st.warning("Silakan login terlebih dahulu.")
    else:
        groups = get_groups(st.session_state.token)
        rooms = get_rooms(st.session_state.token)
        st.metric("Jumlah Grup", len(groups))
        st.metric("Jumlah Room", len(rooms))


# Grup
elif st.session_state.page == "group":
    st.title("📁 Data Grup")
    if not st.session_state.token:
        st.warning("Silakan login.")
    else:
        groups = get_groups(st.session_state.token)

        if not groups:
            st.info("Belum ada grup yang tersedia.")
        else:
            col1, col2 = st.columns([2, 2])
            with col1:
                keyword = st.text_input("Kata kunci")
            with col2:
                search_field = st.selectbox("Filter berdasarkan", ["Nama Grup", "ID", "Dibuat Oleh", "Room ID"])

            field_mapping = {
                "Nama Grup": "nama_grup",
                "ID": "grupid",
                "Dibuat Oleh": "created_by",
                "Room ID": "roomid"
            }

            selected_field = field_mapping[search_field]

            filtered_groups = [g for g in groups if keyword.lower() in str(g.get(selected_field, "")).lower()]

            if not filtered_groups:
                st.warning("Tidak ditemukan hasil pencarian.")
            else:
                df = pd.DataFrame([{
                    "No.": idx + 1,
                    "Nama Grup": g["nama_grup"],
                    "ID Grup": g["grupid"],
                    "Dibuat Oleh": g["created_by"],
                    "Kode Gabung": g["joinCode"],
                    "Room Id": g["roomid"] if g["roomid"] else "Belum Diassign"
                } for idx, g in enumerate(filtered_groups)])

                gb = GridOptionsBuilder.from_dataframe(df)
                gb.configure_pagination(paginationAutoPageSize=True)
                gb.configure_default_column(groupable=False, editable=False)
                gb.configure_grid_options(domLayout='normal')
                gb.configure_grid_options(enableCellTextSelection=True)
                gridOptions = gb.build()

                st.markdown(
                    """
                    <style>
                    .ag-theme-streamlit {
                        font-family: 'Montserrat', sans-serif;
                        font-size: 13px;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                AgGrid(
                    df,
                    gridOptions=gridOptions,
                    height=400,
                    theme="streamlit",  # Other themes: "alpine", "balham", "material"
                    enable_enterprise_modules=False
                )

#Room
elif st.session_state.page == "room":
    st.title("🎧 Data Room")
    if not st.session_state.token:
        st.warning("Silakan login.")
    else:
        rooms = get_rooms(st.session_state.token)

        if not rooms:
            st.info("Belum ada room yang tersedia.")
        else:
            # --- FILTER UI ---
            col1, col2 = st.columns([2, 2])
            with col1:
                keyword = st.text_input("Kata kunci")
            with col2:
                filter_field = st.selectbox("Filter berdasarkan", ["Nama Room", "Id Room"])

            field_map = {
                "Nama Room": "nama_room",
                "Id Room": "id"
            }

            selected_key = field_map[filter_field]
            filtered_rooms = [r for r in rooms if keyword.lower() in str(r.get(selected_key, "")).lower()]

            # --- KONVERSI KE DATAFRAME ---
            df = pd.DataFrame([{
                "No.": idx + 1,
                "Nama Room": r["nama_room"],
                "Id Room": r["id"],
                "Token Speaker": "✅" if r["token_speaker"] else "❌",
                "Token Listener": "✅" if r["token_listener"] else "❌"
            } for idx, r in enumerate(filtered_rooms)])

            # --- AGGRID OPTIONS ---
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_default_column(groupable=False, editable=False)
            gb.configure_grid_options(domLayout='normal')
            gb.configure_grid_options(enableCellTextSelection=True)
            gridOptions = gb.build()

            # --- FONT CUSTOMIZATION ---
            st.markdown("""
                <style>
                .ag-theme-streamlit {
                    font-family: 'Montserrat', sans-serif;
                    font-size: 13px;
                }
                </style>
            """, unsafe_allow_html=True)

            # --- TAMPILKAN AGGRID ---
            AgGrid(
                df,
                gridOptions=gridOptions,
                height=400,
                theme="streamlit",  # Pilihan lain: alpine, balham, material
                enable_enterprise_modules=False
            )

# Halaman Manage
elif st.session_state.page == "manage":
    st.title("🛠️ Buat Grup")

    if not st.session_state.token:
        st.warning("Silakan login.")
    else:
        selected_date = st.date_input("Pilih Tanggal Keberangkatan", min_value=datetime.today())
        nama_grup = f"Grup {selected_date.strftime('%d %B %Y')}"

        st.markdown(f"**Nama Grup:** `{nama_grup}`")

        if st.button("Buat Grup"):
            with st.spinner("Mengecek dan membuat grup..."):
                token = st.session_state.token
                user_id = st.session_state.user["id"]

                # Ambil data grup dan room untuk pengecekan duplikat
                existing_groups = get_groups(token)
                existing_rooms = get_rooms(token)

                if any(g["nama_grup"].lower() == nama_grup.lower() for g in existing_groups):
                    st.error("❌ Grup dengan nama yang sama sudah ada.")
                    st.stop()

                if any(r["nama_room"].lower() == nama_grup.lower() for r in existing_rooms):
                    st.error("❌ Room dengan nama yang sama sudah ada.")
                    st.stop()

                # 1. Buat room
                room = generate_room(nama_grup, token)
                if not room or "id" not in room:
                    st.error("Gagal membuat room.")
                    st.stop()

                # 2. Buat grup
                grup = create_group(nama_grup, user_id, token)
                if not grup or "grupid" not in grup:
                    st.error("Gagal membuat grup.")
                    st.stop()

                # 3. Refresh token room
                refreshed_room = refresh_token(room["id"], token)
                if not refreshed_room:
                    st.error("Gagal me-refresh token room.")
                    st.stop()

                # 4. Assign room ke grup
                assign = assign_room(room["id"], grup["grupid"], token)
                if not assign or assign.get("status") != "success":
                    st.error("Gagal menghubungkan room ke grup.")
                    st.stop()

                st.success("✅ Grup dan Room berhasil dibuat dan dihubungkan.")

# Profile
elif st.session_state.page == "profile":
    st.title("👤 Profil")

    if not st.session_state.token:
        st.warning("Silakan login.")
    else:
        profile = get_profile(st.session_state.token)

        # Ambil foto user (jika null, fallback hanya untuk tampilan)
        photo_url = profile.get("profile", {}).get("photo") or "https://i.pinimg.com/736x/8d/b5/a2/8db5a20a2b2855c3cf256600fb18470d.jpg"

        # Tampilkan gambar profil sebagai lingkaran
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                <img src="{photo_url}" style="border-radius: 50%; width: 200px; height: 200px;" />
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("""
    <h3 style='text-align: center;'>Informasi Akun</h3>
""", unsafe_allow_html=True)
        st.markdown(f"""
    <style>
        .center-container {{
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }}
        .profile-card {{
            background-color: #f9f9f9;
            padding: 25px 35px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            font-family: 'Montserrat', sans-serif;
            width: 100%;
            max-width: 500px;
        }}
        .profile-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .profile-row:last-child {{
            border-bottom: none;
        }}
        .label {{
            font-weight: 600;
            color: #333;
            font-size: 15x;
        }}
        .value {{
            color: #555;
            font-size: 13px;
        }}
    </style>

    <div class="center-container">
        <div class="profile-card">
            <div class="profile-row">
                <div class="label">Nama</div><div class="value">{profile.get("name")}</div>
            </div>
            <div class="profile-row">
                <div class="label">ID Pengguna</div><div class="value">{profile.get("id")}</div>
            </div>
            <div class="profile-row">
                <div class="label">Email</div><div class="value">{profile.get("email")}</div>
            </div>
            <div class="profile-row">
                <div class="label">Whatsapp</div><div class="value">{profile.get("whatsapp")}</div>
            </div>
            <div class="profile-row">
                <div class="label">Role</div><div class="value">{profile.get("role")}</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
