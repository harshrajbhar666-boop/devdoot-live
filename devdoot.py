import streamlit as st
import pandas as pd
import datetime
import time
import sys
import base64
from io import StringIO
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# BLOCK 1: CONFIG & GOOGLE SHEETS CONNECTION
# ==========================================
st.set_page_config(page_title="Devdoot HQ", page_icon="🦅", layout="wide")

# Connect to Google Sheets
def connect_db():
    try:
        # Load credentials from Streamlit Secrets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = dict(st.secrets["gcp_service_account"]) # Secrets se key lo
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        # Open the Sheet
        sheet = client.open("Devdoot_Database")
        return sheet
    except Exception as e:
        st.error(f"❌ Database Connection Failed: {e}")
        return None

# Load Data from Specific Tab
def load_data(sheet_name):
    sh = connect_db()
    if sh:
        worksheet = sh.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    return pd.DataFrame()

# Save New Row to Sheet
def add_row(sheet_name, row_data):
    sh = connect_db()
    if sh:
        worksheet = sh.worksheet(sheet_name)
        worksheet.append_row(row_data)

# Update Cell (For Level/XP/Password)
def update_cell(username, col_name, new_value):
    sh = connect_db()
    if sh:
        ws = sh.worksheet("Users")
        # Find row number
        cell = ws.find(username)
        if cell:
            # Col Mapping: Username=1, Password=2, Role=3, Level=4, XP=5
            col_map = {"Password": 2, "Level": 4, "XP": 5}
            ws.update_cell(cell.row, col_map[col_name], new_value)

# ==========================================
# BLOCK 2: UI & CSS (Iron Man Style)
# ==========================================
# ... (Video Background Code Same as Before - Keep "background.mp4" in repo) ...
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{ background: rgba(0,0,0,0); }}
            .bg-video {{
                position: fixed; top: 0; left: 0; min-width: 100%; min-height: 100%;
                z-index: -1; opacity: 0.85; object-fit: cover;
            }}
            </style>
            <video autoplay muted loop id="myVideo" class="bg-video">
                <source src="data:video/mp4;base64,{encoded_string.decode()}" type="video/mp4">
            </video>
            """, unsafe_allow_html=True
        )
    except:
        pass # Agar video nahi mili to ignore karo

add_bg_from_local("background.mp4")

# Load CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@500;800&display=swap');
    html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; color: #ffffff; }
    h1, h2, h3 { 
        background: linear-gradient(to right, #00c6ff, #0072ff); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; text-transform: uppercase; margin-bottom: 20px;
    }
    .stButton>button {
        background: rgba(0,0,0,0.6); color: #00c6ff; border: 1px solid #00c6ff;
        border-radius: 50px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00c6ff; color: black; box-shadow: 0 0 20px #00c6ff; transform: scale(1.05);
    }
    [data-testid="stImage"] img { border-radius: 50% !important; border: 3px solid #00c6ff; aspect-ratio: 1/1; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCK 3: MODULES (Content)
# ==========================================
MODULES = {
    1: {"title": "MODULE 1: GENESIS", "content": "### Variables\n`x = 10`", "quiz": {"q": "Invalid var?", "options": ["_a", "1a", "a1"], "ans": "1a"}},
    2: {"title": "MODULE 2: LOGIC", "content": "### If-Else\n`if True: pass`", "quiz": {"q": "Else runs when if is?", "options": ["True", "False"], "ans": "False"}}
    # ... (Aur modules yahan add kar sakte hain) ...
}

# ==========================================
# BLOCK 4: LOGIN SYSTEM
# ==========================================
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown("<h2 style='text-align:center'>IDENTITY VERIFICATION</h2>", unsafe_allow_html=True)
        
        # Load Users from Sheet
        try:
            users_df = load_data("Users")
            usernames = users_df['Username'].tolist() if not users_df.empty else ["Devdoot"]
        except:
            usernames = ["System Error"]
            st.error("Database Connection Error. Check Secrets.")

        u = st.selectbox("SELECT AGENT", usernames)
        p = st.text_input("SECURITY CODE", type="password")
        
        if st.button("AUTHENTICATE"):
            user_row = users_df[users_df['Username'] == u]
            if not user_row.empty:
                real_pass = str(user_row.iloc[0]['Password'])
                if p == real_pass:
                    st.session_state.update({
                        "logged_in": True, "user": u, 
                        "role": user_row.iloc[0]['Role'],
                        "level": int(user_row.iloc[0]['Level']),
                        "xp": int(user_row.iloc[0]['XP'])
                    })
                    st.toast("✅ ACCESS GRANTED", icon="🔐")
                    time.sleep(1)
                    st.rerun()
                else: st.error("⚠️ WRONG PASSWORD")
            else: st.error("USER NOT FOUND")
    st.stop()

# ==========================================
# BLOCK 5: MAIN DASHBOARD
# ==========================================
# Universal Header
c1, c2, c3 = st.columns([1,8,1])
with c1: st.image("logo.png", width=80)
with c2: 
    st.markdown(f"### WELCOME AGENT {st.session_state['user']} | LEVEL {st.session_state['level']}")
    st.progress(min(st.session_state['level']*20, 100))
with c3:
    if st.button("⏻"): st.session_state["logged_in"] = False; st.rerun()

st.divider()
tabs = st.tabs(["📊 DASHBOARD", "📝 ATTENDANCE", "🧠 TRAINING", "⚙️ SETTINGS"])

# --- TAB 1: DASHBOARD ---
with tabs[0]:
    st.title("COMMAND CENTER")
    c1, c2, c3 = st.columns(3)
    c1.metric("YOUR XP", f"{st.session_state['xp']}", "Total")
    
    # Live Data from Sheet
    att_df = load_data("Attendance")
    # IST Time Calculation
    ist_now = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")
    
    present_count = att_df[att_df['Date'] == today].shape[0] if not att_df.empty else 0
    c2.metric("SQUAD STATUS", f"{present_count}/6", "Online Today")
    c3.metric("DATABASE", "GOOGLE CLOUD", "Connected 🟢")

# --- TAB 2: ATTENDANCE ---
with tabs[1]:
    st.title("DAILY LOG")
    if st.button("MARK PRESENCE"):
        att_df = load_data("Attendance")
        ist_now = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
        today = ist_now.strftime("%Y-%m-%d")
        time_now = ist_now.strftime("%H:%M:%S")
        
        # Check Duplicate
        if not att_df.empty and not att_df[(att_df['Name'] == st.session_state['user']) & (att_df['Date'] == today)].empty:
            st.toast("ALREADY LOGGED", icon="🛑")
        else:
            # Add to Sheet
            add_row("Attendance", [today, time_now, st.session_state['user'], "Present"])
            st.toast(f"LOGGED AT {time_now}", icon="📍")
            time.sleep(1); st.rerun()
            
    st.dataframe(load_data("Attendance"), use_container_width=True)

# --- TAB 3: TRAINING ---
with tabs[2]:
    st.title("ACADEMY")
    for i in range(1, 3): # Demo 2 modules
        d = MODULES[i]
        with st.expander(d['title']):
            st.markdown(d['content'])
            ans = st.radio("Quiz:", d['quiz']['options'], key=i)
            if st.button(f"Submit {i}"):
                if ans == d['quiz']['ans']:
                    st.toast("CORRECT! +50 XP")
                    new_xp = st.session_state['xp'] + 50
                    # Update Local & Sheet
                    st.session_state['xp'] = new_xp
                    update_cell(st.session_state['user'], "XP", new_xp)
                    time.sleep(1); st.rerun()
                else: st.error("Wrong")

# --- TAB 4: SETTINGS ---
with tabs[3]:
    new_p = st.text_input("New Password", type="password")
    if st.button("Update"):
        update_cell(st.session_state['user'], "Password", new_p)
        st.success("Password Saved to Cloud.")
