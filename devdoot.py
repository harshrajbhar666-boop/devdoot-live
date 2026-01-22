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
# BLOCK 1: CONFIG & DATABASE ENGINE ⚙️
# ==========================================
st.set_page_config(page_title="Devdoot HQ", page_icon="🦅", layout="wide")

# --- 1. GOOGLE SHEETS CONNECTION ---
def connect_db():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = dict(st.secrets["gcp_service_account"]) 
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client.open("Devdoot_Database")
    except Exception as e:
        st.error(f"❌ DB Error: {e}")
        return None

# --- 2. HELPER FUNCTIONS ---
def get_ist_time():
    return datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)

def load_data(sheet_name):
    sh = connect_db()
    if sh:
        try:
            worksheet = sh.worksheet(sheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except: return pd.DataFrame() # Return empty if sheet error
    return pd.DataFrame()

def add_row(sheet_name, row_data):
    sh = connect_db()
    if sh:
        sh.worksheet(sheet_name).append_row(row_data)

def update_xp_level(username, new_lvl, new_xp):
    sh = connect_db()
    if sh:
        ws = sh.worksheet("Users")
        cell = ws.find(username)
        if cell:
            ws.update_cell(cell.row, 4, new_lvl) # Col 4 = Level
            ws.update_cell(cell.row, 5, new_xp)  # Col 5 = XP

def update_password(username, new_pass):
    sh = connect_db()
    if sh:
        ws = sh.worksheet("Users")
        cell = ws.find(username)
        if cell: ws.update_cell(cell.row, 2, new_pass) # Col 2 = Password

# ==========================================
# BLOCK 2: THE IRON MAN UI (CSS MAGIC) 🎨
# ==========================================
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
    except: pass

add_bg_from_local("background.mp4")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@500;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Exo 2', sans-serif;
        color: #ffffff;
    }

    /* --- HEADINGS --- */
    h1, h2, h3 {
        background: linear-gradient(90deg, rgba(0,0,0,0.8), rgba(0,0,0,0));
        border-left: 5px solid #00c6ff;
        padding: 10px 20px;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    /* --- CIRCULAR LOGO --- */
    [data-testid="stImage"] img {
        border-radius: 50% !important;
        border: 3px solid #00c6ff;
        box-shadow: 0 0 15px #00c6ff;
        object-fit: cover !important;
        aspect-ratio: 1 / 1;
    }

    /* --- POWER BUTTON (RED) --- */
    div[data-testid="column"] .stButton button p:contains("⏻") {
        color: #FF0000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }
    
    /* --- CAPSULE BUTTONS --- */
    .stButton>button {
        background: rgba(0,0,0,0.6);
        color: #00c6ff;
        border: 1px solid #00c6ff;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00c6ff;
        color: black;
        box-shadow: 0 0 20px #00c6ff;
        transform: scale(1.05);
    }

    /* --- TABS DESIGN --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        padding: 15px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 50px;
        background-color: rgba(0,0,0,0.8);
        color: #aaa;
        border: 1px solid #333;
        padding: 0 25px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white !important;
        border: 1px solid #fff;
        box-shadow: 0 0 15px #00c6ff;
    }
    
    /* --- GLASS CARDS --- */
    .stMetric, .stDataFrame, .stExpander {
        background: rgba(0,0,0,0.6);
        border: 1px solid rgba(0, 198, 255, 0.3);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# --- TAB 3: TRAINING (UPGRADED UI) ---
with tabs[2]:
    st.title("ACADEMY OF CODE")
    st.markdown("*> Complete missions in the Code Lab, then pass the Quiz to level up.*")
    
    mod_tabs = st.tabs([f"MOD {i}" for i in MODULES])
    
    for i, tab in enumerate(mod_tabs):
        m = i + 1
        with tab:
            if lvl < m: 
                st.error(f"🔒 ACCESS DENIED. CLEAR MODULE {m-1} TO UNLOCK.")
                st.image("https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif", width=300) # Optional Lock GIF
            else:
                d = MODULES[m]
                
                # 1. THEORY SECTION
                st.markdown(f"## {d['title']}")
                st.info("📖 STUDY MATERIAL")
                st.markdown(d['theory'])
                st.divider()
                
                # 2. MISSION SECTION
                st.error("💀 PRACTICAL MISSION")
                st.markdown(d['mission'])
                
                # 3. HINT SYSTEM
                with st.expander("💡 STUCK? OPEN TACTICAL HINT"):
                    st.warning(f"**INTEL:** {d['hint']}")
                
                st.divider()
                
                # 4. QUIZ SECTION
                st.success("✅ SYSTEM CHECK (GET XP)")
                q = d['quiz']
                st.write(f"**Q:** {q['q']}")
                ans = st.radio("Select Protocol:", q['options'], key=m)
                
                if st.button(f"SUBMIT DATA {m}"):
                    if ans == q['quiz']['ans'] if isinstance(q, dict) and 'quiz' in q else q['ans']: # Safety check
                        st.balloons()
                        st.toast(f"MISSION ACCOMPLISHED! +100 XP", icon="🎖️")
                        
                        # Logic to prevent farming XP on same level
                        if st.session_state['level'] == m:
                             st.session_state['xp'] += 100
                             st.session_state['level'] = m + 1
                             update_xp_level(user, m+1, st.session_state['xp'])
                             time.sleep(2); st.rerun()
                        else:
                            st.info("Already Completed. Reviewing material allowed.")
                    else: 
                        st.toast("❌ ACCESS DENIED. INCORRECT ANSWER.", icon="⚠️")

# ==========================================
# BLOCK 4: LOGIN SYSTEM 🔐
# ==========================================
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown("""<div style='background: rgba(0,0,0,0.8); padding: 30px; border-radius: 20px; border: 1px solid #00c6ff; text-align: center;'>
            <h2>IDENTITY VERIFICATION</h2></div>""", unsafe_allow_html=True)
        
        # Load Users from Sheet
        try:
            users_df = load_data("Users")
            if not users_df.empty:
                # Ensure columns are strings to avoid KeyErrors
                users_df.columns = users_df.columns.str.strip() 
                usernames = users_df['Username'].tolist()
            else:
                usernames = ["Database Empty"]
        except:
            usernames = ["Connection Error"]
            st.error("Google Sheet Connection Failed. Check Secrets.")

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
# BLOCK 5: MAIN DASHBOARD 🦅
# ==========================================
user = st.session_state['user']
lvl = st.session_state['level']
xp = st.session_state['xp']

# --- HEADER ---
top_col1, top_col2, top_col3 = st.columns([1, 8, 1])
with top_col1: st.image("logo.png", width=80)
with top_col2:
    st.markdown(f"<h3 style='margin:0; font-size: 20px; text-align: left;'>WELCOME, AGENT {user} | LEVEL {lvl}</h3>", unsafe_allow_html=True)
    st.progress(min(lvl*16, 100))
with top_col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⏻"):
        st.session_state["logged_in"] = False
        st.rerun()

st.divider()

# --- TABS ---
tab_names = ["📊 DASHBOARD", "💻 CODE LAB", "🧠 TRAINING", "📝 ATTENDANCE", "⚙️ SETTINGS"]
if st.session_state['role'] == "Admin": tab_names.append("👁️ GOD VIEW")
tabs = st.tabs(tab_names)

# --- TAB 1: DASHBOARD ---
with tabs[0]:
    st.title("COMMAND CENTER")
    c1, c2, c3 = st.columns(3)
    c1.metric("YOUR XP", f"{xp}", "Total")
    
    # Live Data
    att_df = load_data("Attendance")
    today = get_ist_time().strftime("%Y-%m-%d")
    present_count = att_df[att_df['Date'] == today].shape[0] if not att_df.empty else 0
    
    c2.metric("SQUAD STATUS", f"{present_count}/6", "Online Today")
    c3.metric("DATABASE", "GOOGLE CLOUD", "Connected 🟢")

# --- TAB 2: CODE LAB ---
with tabs[1]:
    st.title("PYTHON IDE")
    col_code, col_out = st.columns([1, 1])
    with col_code:
        st.markdown("### 📝 EDITOR")
        code = st.text_area("Write Python Code:", height=300, value="# Practice here\nprint('Devdoot HQ')")
        b1, b2 = st.columns([1, 1])
        with b1: run = st.button("▶ RUN CODE")
        with b2: st.download_button(label="💾 SAVE FILE", data=code, file_name="mission.py", mime="text/x-python")
    with col_out:
        st.markdown("### 📟 TERMINAL OUTPUT")
        if run:
            redirected_output = sys.stdout = StringIO()
            try: 
                exec(code)
                st.code(redirected_output.getvalue())
                st.toast("Executed Successfully", icon="✅")
            except Exception as e: st.error(f"RUNTIME ERROR:\n{e}")

# --- TAB 3: TRAINING ---
with tabs[2]:
    st.title("ACADEMY")
    mod_tabs = st.tabs([f"MOD {i}" for i in MODULES])
    for i, tab in enumerate(mod_tabs):
        m = i + 1
        with tab:
            if lvl < m: st.error(f"🔒 LOCKED. FINISH MODULE {m-1} FIRST.")
            else:
                d = MODULES[m]
                st.markdown(d['content'])
                st.divider()
                st.subheader("QUIZ PROTOCOL")
                q = d['quiz']
                st.write(f"**Q:** {q['q']}")
                ans = st.radio("Select:", q['options'], key=m)
                if st.button(f"SUBMIT ANSWER {m}"):
                    if ans == q['ans']:
                        st.toast(f"CORRECT! +50 XP", icon="🏆")
                        # Update Local & DB
                        st.session_state['xp'] += 50
                        st.session_state['level'] = m + 1
                        update_xp_level(user, m+1, st.session_state['xp'])
                        time.sleep(1); st.rerun()
                    else: st.toast("NEGATIVE.", icon="❌")

# --- TAB 4: ATTENDANCE ---
with tabs[3]:
    st.title("DAILY LOG")
    if st.button("MARK PRESENCE"):
        att_df = load_data("Attendance")
        ist_now = get_ist_time()
        today_str = ist_now.strftime("%Y-%m-%d")
        time_str = ist_now.strftime("%H:%M:%S")
        
        # Check Duplicate
        if not att_df.empty and not att_df[(att_df['Name'] == user) & (att_df['Date'] == today_str)].empty:
            st.toast("ALREADY LOGGED", icon="🛑")
        else:
            add_row("Attendance", [today_str, time_str, user, "Present"])
            st.toast(f"LOGGED AT {time_str}", icon="📍")
            time.sleep(1); st.rerun()
    
    st.dataframe(load_data("Attendance"), use_container_width=True)

# --- TAB 5: SETTINGS ---
with tabs[4]:
    st.title("SETTINGS")
    new_p = st.text_input("NEW PASSWORD", type="password")
    if st.button("UPDATE CREDENTIALS"):
        update_password(user, new_p)
        st.toast("PASSWORD SAVED TO CLOUD", icon="☁️")

# --- TAB 6: GOD VIEW ---
if st.session_state['role'] == "Admin":
    with tabs[5]:
        st.title("👁️ GOD VIEW")
        st.markdown("### 👥 All Agents")
        st.dataframe(load_data("Users"), use_container_width=True)
        st.markdown("### 📝 Full Attendance Log")
        st.dataframe(load_data("Attendance"), use_container_width=True)

