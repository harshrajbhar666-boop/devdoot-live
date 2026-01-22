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
# BLOCK 2: THE IRON MAN UI (GLASSMORPHISM EDITION) 🎨
# ==========================================
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        st.markdown(
            f"""
            <style>
            /* Make the main app background transparent */
            .stApp {{ background: rgba(0,0,0,0); }}
            /* Fixed background video */
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
    html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; color: #ffffff; }

    /* --- GLASSMORPHISM CONTENT BOX --- */
    /* This targets the main content area of Streamlit */
    .stApp > header + div {
        background-color: rgba(0, 0, 0, 0.75); /* Dark semi-transparent background */
        backdrop-filter: blur(15px); /* The blur effect */
        -webkit-backdrop-filter: blur(15px); /* For Safari */
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
        box-shadow: 0 8px 32px 0 rgba(0, 198, 255, 0.3); /* Glowing shadow */
        margin: 20px auto; /* Center it */
        max-width: 95%; /* Leave some space on sides */
    }

    /* --- HEADINGS --- */
    h1, h2, h3 {
        background: linear-gradient(90deg, rgba(0,0,0,0.8), rgba(0,0,0,0));
        border-left: 5px solid #00c6ff; padding: 10px 20px;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px;
    }
    /* --- LOGO & BUTTONS --- */
    [data-testid="stImage"] img { border-radius: 50% !important; border: 3px solid #00c6ff; box-shadow: 0 0 15px #00c6ff; object-fit: cover !important; aspect-ratio: 1 / 1; }
    div[data-testid="column"] .stButton button p:contains("⏻") { color: #FF0000 !important; font-size: 24px !important; font-weight: 900 !important; }
    .stButton>button { background: rgba(0,0,0,0.6); color: #00c6ff; border: 1px solid #00c6ff; border-radius: 50px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background: #00c6ff; color: black; box-shadow: 0 0 20px #00c6ff; transform: scale(1.05); }
    
    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: transparent; padding: 15px; justify-content: center; border-bottom: none; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 50px; background-color: rgba(0,0,0,0.5); color: #aaa; border: 1px solid #333; padding: 0 25px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(90deg, #00c6ff, #0072ff); color: white !important; border: 1px solid #fff; box-shadow: 0 0 15px #00c6ff; }
    
    /* --- GLASS CARDS INSIDE --- */
    .stMetric, .stDataFrame, .stExpander { background: rgba(0,0,0,0.4) !important; border: 1px solid rgba(0, 198, 255, 0.3) !important; border-radius: 10px; }
    div[data-testid="stExpander"]details { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCK 3: ADVANCED ACADEMY MODULES (HARDCORE MODE) 🎓
# ==========================================
MODULES = {
    1: {
        "title": "MODULE 1: DATA STREAMS (VARIABLES & I/O)",
        "theory": "### 📡 DEEP DIVE: The Memory Matrix\nVariables are labels pointing to memory.\n\n**Critical Concepts:**\n1. **Dynamic Typing:** `x=10` (int), `x='10'` (str).\n2. **Type Casting:** `int('5') + 5 = 10`.\n3. **f-Strings:** `print(f'Agent {name}')`.\n\n**⚠️ Trap:** `input()` always gives a STRING.",
        "mission": "**⚔️ OPS MISSION: THE ID GENERATOR**\n1. Ask for `Agent Name`.\n2. Ask for `Birth Year`.\n3. Calculate `Age`.\n4. Generate Code: First 3 letters of Name + Age.\n5. Print: `Identity: [Code] // Verified`",
        "hint": "Use `int()` for year. Use `name[0:3]` for slicing.",
        "quiz": {"q": "Output of: print(f'{10+5}' + '0')?", "options": ["150", "1050", "Error"], "ans": "150"}
    },
    2: {
        "title": "MODULE 2: LOGIC GATES (CONDITIONAL WARFARE)",
        "theory": "### 📡 DEEP DIVE: Decision Trees\n**Operators:** `and`, `or`, `not`.\n\n**Nested Logic:**\n```python\nif id_card:\n    if finger_print:\n        print('Access')\n```",
        "mission": "**⚔️ OPS MISSION: BUNKER SECURITY**\nCheck 3 variables:\n1. `key_card` (True)\n2. `pass_code` ('1234')\n3. `bio_scan` (>80)\n\n* All Pass -> 'Welcome'\n* Fail -> 'Alarm'",
        "hint": "Use `if key and code == '1234':`",
        "quiz": {"q": "Result of: True or False and False?", "options": ["True", "False", "Error"], "ans": "True"}
    },
    3: {
        "title": "MODULE 3: INFINITE CYCLES (LOOPS)",
        "theory": "### 📡 DEEP DIVE: Automating Chaos\n**Range:** `range(start, stop, step)`.\n**Control:** `break` (Stop), `continue` (Skip).\n\n**While Loops:** Run until condition becomes False.",
        "mission": "**⚔️ OPS MISSION: THE BRUTE FORCE**\n1. `secret = 7`\n2. Loop 1 to 10.\n3. If match -> Print 'Cracked' & BREAK.\n4. Else -> Print 'Scanning...'",
        "hint": "Use `for i in range(1, 11):` and `if i == secret: break`.",
        "quiz": {"q": "What does 'continue' do?", "options": ["Stops loop", "Skips iteration", "Restarts loop"], "ans": "Skips iteration"}
    },
    4: {
        "title": "MODULE 4: THE ARMORY (LISTS)",
        "theory": "### 📡 DEEP DIVE: Inventory\n**Slicing:** `data[0:3]`, `data[::-1]` (Reverse).\n**Methods:** `.append()`, `.pop()`, `.remove()`.",
        "mission": "**⚔️ OPS MISSION: WEAPON LOADOUT**\n1. `loadout = ['Pistol', 'Knife', 'Smoke']`\n2. Add 'Sniper'.\n3. Remove 'Knife'.\n4. Insert 'Grenade' at index 1.\n5. Print LAST weapon.",
        "hint": "Last item is `list[-1]`. Use `.insert(1, 'Item')`.",
        "quiz": {"q": "list.pop(1) removes which index?", "options": ["0", "1", "Last"], "ans": "1"}
    },
    5: {
        "title": "MODULE 5: PROTOCOLS (FUNCTIONS)",
        "theory": "### 📡 DEEP DIVE: Modular Code\nFunctions take arguments and return values.\n`def attack(power=100):` (Default value).",
        "mission": "**⚔️ OPS MISSION: DAMAGE CALC**\n1. Define `calc_dmg(base, mult)`.\n2. Return `base * mult`.\n3. Call with (50, 1.5).",
        "hint": "Use `def`, `return`. Don't forget to print the result.",
        "quiz": {"q": "Variables inside functions are?", "options": ["Global", "Local"], "ans": "Local"}
    },
    6: {
        "title": "MODULE 6: FAILSAFE (ERRORS)",
        "theory": "### 📡 DEEP DIVE: Safety\n`try` (Risk), `except` (Safety), `finally` (Always).\nCatch `ValueError` or `ZeroDivisionError`.",
        "mission": "**⚔️ OPS MISSION: SAFE DIVIDER**\n1. Input `a`, `b`.\n2. Print `a / b`.\n3. Catch `ZeroDivisionError` (if b=0).\n4. Catch `ValueError` (if text).",
        "hint": "Wrap input/print in `try:`. Use `except:` blocks below.",
        "quiz": {"q": "Code in 'finally' runs...", "options": ["On Error", "Always"], "ans": "Always"}
    }
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
        # Glassmorphism effect is applied by the global CSS
        st.markdown("""<div style='text-align: center;'>
            <h2>IDENTITY VERIFICATION</h2></div>""", unsafe_allow_html=True)
        
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

# --- TABS CREATION ---
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
    c2.metric("SQUAD STATUS", f"{present_count}/6", "Online Today")
    c3.metric("DATABASE", "GOOGLE CLOUD", "Connected 🟢")

# --- TAB 2: CODE LAB ---
with tabs[1]:
    st.title("PYTHON IDE")
    col_code, col_out = st.columns([1, 1])
    with col_code:
        st.markdown("### 📝 EDITOR")
        code = st.text_area("Write Python Code:", height=300, value="# Practice here\nprint('Devdoot HQ')")
        if st.button("▶ RUN CODE"):
            st.session_state['run_code'] = code
    with col_out:
        st.markdown("### 📟 TERMINAL OUTPUT")
        if 'run_code' in st.session_state:
            redirected_output = sys.stdout = StringIO()
            try: 
                exec(st.session_state['run_code'])
                st.code(redirected_output.getvalue())
                st.toast("Executed Successfully", icon="✅")
            except Exception as e: st.error(f"RUNTIME ERROR:\n{e}")

# --- TAB 3: TRAINING (HARDCORE MODE) ---
with tabs[2]:
    st.title("ACADEMY OF CODE")
    st.markdown("*> Complete missions in Code Lab, then pass Quiz.*")
    mod_tabs = st.tabs([f"MOD {i}" for i in MODULES])
    
    for i, tab in enumerate(mod_tabs):
        m = i + 1
        with tab:
            if lvl < m: 
                st.error(f"🔒 ACCESS DENIED. CLEAR MODULE {m-1} FIRST.")
            else:
                d = MODULES[m]
                st.markdown(f"## {d['title']}")
                st.info("📖 STUDY MATERIAL")
                st.markdown(d['theory'])
                st.divider()
                st.error("💀 PRACTICAL MISSION")
                st.markdown(d['mission'])
                with st.expander("💡 TACTICAL HINT"):
                    st.warning(f"**INTEL:** {d['hint']}")
                st.divider()
                st.success("✅ SYSTEM CHECK")
                q = d['quiz']
                st.write(f"**Q:** {q['q']}")
                ans = st.radio("Select Protocol:", q['options'], key=m)
                
                if st.button(f"SUBMIT DATA {m}"):
                    if ans == q['ans']:
                        st.balloons()
                        st.toast(f"MISSION ACCOMPLISHED! +100 XP", icon="🎖️")
                        if st.session_state['level'] == m:
                             st.session_state['xp'] += 100
                             st.session_state['level'] = m + 1
                             update_xp_level(user, m+1, st.session_state['xp'])
                             time.sleep(2); st.rerun()
                        else: st.info("Already Completed.")
                    else: st.toast("❌ ACCESS DENIED.", icon="⚠️")

# --- TAB 4: ATTENDANCE ---
with tabs[3]:
    st.title("DAILY LOG")
    if st.button("MARK PRESENCE"):
        att_df = load_data("Attendance")
        ist_now = get_ist_time()
        today_str, time_str = ist_now.strftime("%Y-%m-%d"), ist_now.strftime("%H:%M:%S")
        if not att_df.empty and not att_df[(att_df['Name'] == user) & (att_df['Date'] == today_str)].empty:
            st.toast("ALREADY LOGGED", icon="🛑")
        else:
            add_row("Attendance", [today_str, time_str, user, "Present"])
            st.toast(f"LOGGED AT {time_str}", icon="📍"); time.sleep(1); st.rerun()
    st.dataframe(load_data("Attendance"), use_container_width=True)

# --- TAB 5: SETTINGS ---
with tabs[4]:
    st.title("SETTINGS")
    new_p = st.text_input("NEW PASSWORD", type="password")
    if st.button("UPDATE CREDENTIALS"):
        update_password(user, new_p)
        st.toast("PASSWORD SAVED", icon="☁️")

# --- TAB 6: GOD VIEW ---
if st.session_state['role'] == "Admin":
    with tabs[5]:
        st.title("👁️ GOD VIEW")
        st.dataframe(load_data("Users"), use_container_width=True)
        st.dataframe(load_data("Attendance"), use_container_width=True)
