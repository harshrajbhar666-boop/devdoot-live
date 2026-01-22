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
        except: return pd.DataFrame()
    return pd.DataFrame()

def add_row(sheet_name, row_data):
    sh = connect_db()
    if sh:
        try:
            sh.worksheet(sheet_name).append_row(row_data)
        except: pass

def update_xp_level(username, new_lvl, new_xp):
    sh = connect_db()
    if sh:
        ws = sh.worksheet("Users")
        cell = ws.find(username)
        if cell:
            ws.update_cell(cell.row, 4, new_lvl)
            ws.update_cell(cell.row, 5, new_xp)

def update_password(username, new_pass):
    sh = connect_db()
    if sh:
        ws = sh.worksheet("Users")
        cell = ws.find(username)
        if cell: ws.update_cell(cell.row, 2, new_pass)

# ==========================================
# BLOCK 2: THE UI POLISH (CAPSULES & BOX FIX) 🎨
# ==========================================
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{ background: transparent !important; }}
            .bg-video {{
                position: fixed; top: 0; left: 0; min-width: 100%; min-height: 100%;
                z-index: -1; opacity: 1; object-fit: cover;
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
    html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; color: #ffffff; }

    /* --- 1. BOX FIX (Removed Top Cut) --- */
    .block-container {
        background-color: rgba(10, 10, 10, 0.95) !important;
        border: 2px solid #00c6ff;
        border-radius: 20px;
        padding: 3rem !important;
        margin-top: 5rem !important; /* Pushed down to avoid cutting */
        box-shadow: 0 0 50px rgba(0, 198, 255, 0.2);
        max-width: 90% !important;
    }

    /* --- 2. CAPSULE BUTTONS --- */
    .stButton > button {
        background-color: transparent !important;
        color: #00c6ff !important;
        border: 2px solid #00c6ff !important;
        border-radius: 50px !important; /* CAPSULE SHAPE */
        font-weight: bold !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #00c6ff !important;
        color: black !important;
        box-shadow: 0 0 20px #00c6ff !important;
        transform: scale(1.05) !important;
    }

    /* --- HEADINGS --- */
    h1, h2, h3 {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
    }
    
    /* --- INPUT FIELDS --- */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #222 !important; 
        border: 1px solid #444 !important; 
        color: #aaa !important; 
        border-radius: 20px !important; /* Rounded Tabs */
    }
    .stTabs [aria-selected="true"] { 
        background: #00c6ff !important; 
        color: black !important; 
        border: none !important;
    }
    
    /* --- POWER BUTTON --- */
    div[data-testid="column"] .stButton button p:contains("⏻") { color: red !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCK 3: ACADEMY MODULES
# ==========================================
MODULES = {
    1: {"title": "MODULE 1: DATA STREAMS", "theory": "### 📡 The Memory Matrix\nVariables are labels.\n\n**Concepts:**\n1. **Dynamic Typing:** `x=10` vs `x='10'`.\n2. **Casting:** `int('5') + 5 = 10`.\n3. **f-Strings:** `f'Agent {name}'`.\n\n**Trap:** `input()` is always STRING.", "mission": "**⚔️ MISSION: ID GENERATOR**\n1. Input `Name` & `Year`.\n2. Calc `Age`.\n3. Code: First 3 letters of Name + Age.\n4. Print `Identity: [Code]`.", "hint": "Use `int()` for year. `name[0:3]` for slicing.", "quiz": {"q": "print(f'{10+5}' + '0')?", "options": ["150", "1050", "Error"], "ans": "150"}},
    2: {"title": "MODULE 2: LOGIC GATES", "theory": "### 📡 Decision Trees\n**Operators:** `and`, `or`, `not`.\n\n**Nested Logic:**\n`if id_card: if finger_print: ...`", "mission": "**⚔️ MISSION: BUNKER SECURITY**\nCheck:\n1. `key_card` (True)\n2. `pass_code` ('1234')\n3. `bio_scan` (>80)\nPass -> Welcome, Fail -> Alarm.", "hint": "Combine checks: `if key and code == '1234':`", "quiz": {"q": "True or False and False?", "options": ["True", "False"], "ans": "True"}},
    3: {"title": "MODULE 3: INFINITE CYCLES", "theory": "### 📡 Automating Chaos\n**Range:** `range(0, 10)`.\n**Control:** `break` (Stop), `continue` (Skip).\n**While:** Runs while True.", "mission": "**⚔️ MISSION: BRUTE FORCE**\n1. `secret = 7`.\n2. Loop 1-10.\n3. Match -> Print 'Cracked' & BREAK.\n4. Else -> 'Scanning...'", "hint": "`if i == secret: break`", "quiz": {"q": "'continue' does what?", "options": ["Stops loop", "Skips turn"], "ans": "Skips turn"}},
    4: {"title": "MODULE 4: THE ARMORY", "theory": "### 📡 Inventory (Lists)\n**Slicing:** `list[::-1]` (Reverse).\n**Methods:** `.append()`, `.pop()`, `.remove()`.", "mission": "**⚔️ MISSION: LOADOUT**\n1. `['Pistol', 'Knife', 'Smoke']`.\n2. Add 'Sniper'.\n3. Remove 'Knife'.\n4. Insert 'Grenade' at 1.\n5. Print LAST item.", "hint": "Use `list[-1]` for last item.", "quiz": {"q": "list.pop(1) removes index?", "options": ["0", "1", "Last"], "ans": "1"}},
    5: {"title": "MODULE 5: PROTOCOLS", "theory": "### 📡 Functions\nReusable blocks.\n`def attack(dmg=10):`", "mission": "**⚔️ MISSION: DMG CALC**\n1. `def calc(base, mult)`.\n2. Return `base * mult`.\n3. Call (50, 1.5).", "hint": "Don't forget `return`.", "quiz": {"q": "Vars inside functions are?", "options": ["Global", "Local"], "ans": "Local"}},
    6: {"title": "MODULE 6: FAILSAFE", "theory": "### 📡 Error Handling\n`try` (Risk) -> `except` (Safety).\nCatch `ZeroDivisionError`.", "mission": "**⚔️ MISSION: SAFE DIVIDER**\n1. Input a, b.\n2. Print a/b.\n3. Catch `ZeroDivisionError`.\n4. Catch `ValueError`.", "hint": "Wrap inputs in `try:` block.", "quiz": {"q": "'finally' block runs?", "options": ["On Error", "Always"], "ans": "Always"}}
}

# ==========================================
# BLOCK 4: LOGIN SYSTEM 🔐
# ==========================================
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown("<h2 style='text-align:center;'>IDENTITY VERIFICATION</h2>", unsafe_allow_html=True)
        
        try:
            users_df = load_data("Users")
            if not users_df.empty:
                users_df.columns = users_df.columns.str.strip() 
                usernames = users_df['Username'].tolist()
            else: usernames = ["Database Empty"]
        except: usernames = ["Connection Error"]

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
                    time.sleep(1); st.rerun()
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
    att_df = load_data("Attendance")
    today = get_ist_time().strftime("%Y-%m-%d")
    present_count = att_df[att_df['Date'] == today].shape[0] if not att_df.empty else 0
    c2.metric("SQUAD STATUS", f"{present_count}/6", "Online")
    c3.metric("DATABASE", "GOOGLE CLOUD", "Connected 🟢")

# --- TAB 2: CODE LAB (RESTORED SAVE FEATURE) ---
with tabs[1]:
    st.title("PYTHON IDE")
    col_code, col_out = st.columns([1, 1])
    with col_code:
        st.markdown("### 📝 EDITOR")
        code = st.text_area("Write Code:", height=300, value="# Mission Code Here\nprint('Hello Devdoot')")
        
        # --- TWO BUTTONS: RUN & SAVE ---
        b1, b2 = st.columns(2)
        with b1: 
            if st.button("▶ RUN CODE"): st.session_state['run_code'] = code
        with b2:
            if st.button("💾 SAVE TO HQ"):
                ist_now = get_ist_time()
                add_row("Tasks", [ist_now.strftime("%Y-%m-%d"), ist_now.strftime("%H:%M:%S"), user, code])
                st.toast("CODE SAVED TO HQ DATABASE", icon="📡")

    with col_out:
        st.markdown("### 📟 OUTPUT")
        if 'run_code' in st.session_state:
            redirected_output = sys.stdout = StringIO()
            try: 
                exec(st.session_state['run_code'])
                st.code(redirected_output.getvalue())
                st.toast("System: Executed", icon="✅")
            except Exception as e: st.error(f"RUNTIME ERROR:\n{e}")

# --- TAB 3: TRAINING ---
with tabs[2]:
    st.title("ACADEMY")
    st.markdown("*> Finish missions in IDE, then submit Quiz.*")
    mod_tabs = st.tabs([f"MOD {i}" for i in MODULES])
    for i, tab in enumerate(mod_tabs):
        m = i + 1
        with tab:
            if lvl < m: st.error(f"🔒 LOCKED. FINISH MOD {m-1}.")
            else:
                d = MODULES[m]
                st.markdown(f"## {d['title']}")
                st.info("📖 THEORY"); st.markdown(d['theory']); st.divider()
                st.error("💀 MISSION"); st.markdown(d['mission'])
                with st.expander("💡 HINT"): st.warning(d['hint'])
                st.divider()
                st.success("✅ QUIZ")
                ans = st.radio(d['quiz']['q'], d['quiz']['options'], key=m)
                if st.button(f"SUBMIT {m}"):
                    if ans == d['quiz']['ans']:
                        st.balloons(); st.toast("+100 XP")
                        if st.session_state['level'] == m:
                             st.session_state['xp'] += 100; st.session_state['level'] = m + 1
                             update_xp_level(user, m+1, st.session_state['xp']); time.sleep(1); st.rerun()
                    else: st.toast("INCORRECT", icon="❌")

# --- TAB 4: ATTENDANCE ---
with tabs[3]:
    st.title("DAILY LOG")
    if st.button("MARK PRESENCE"):
        att_df = load_data("Attendance")
        ist_now = get_ist_time()
        today, time_now = ist_now.strftime("%Y-%m-%d"), ist_now.strftime("%H:%M:%S")
        if not att_df.empty and not att_df[(att_df['Name'] == user) & (att_df['Date'] == today)].empty:
            st.toast("ALREADY LOGGED", icon="🛑")
        else:
            add_row("Attendance", [today, time_now, user, "Present"])
            st.toast(f"LOGGED AT {time_now}", icon="📍"); time.sleep(1); st.rerun()
    st.dataframe(load_data("Attendance"), use_container_width=True)

# --- TAB 5: SETTINGS ---
with tabs[4]:
    st.title("SETTINGS")
    new_p = st.text_input("NEW PASSWORD", type="password")
    if st.button("UPDATE"): update_password(user, new_p); st.toast("SAVED", icon="☁️")

# --- TAB 6: GOD VIEW (ADDED TASK VIEWER) ---
if st.session_state['role'] == "Admin":
    with tabs[5]:
        st.title("👁️ GOD VIEW")
        st.markdown("### 👥 AGENTS STATUS")
        st.dataframe(load_data("Users"), use_container_width=True)
        
        st.markdown("### 📝 ATTENDANCE LOG")
        st.dataframe(load_data("Attendance"), use_container_width=True)
        
        st.markdown("### 💾 SAVED MISSIONS (CODE)")
        st.dataframe(load_data("Tasks"), use_container_width=True)
