# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:13:57 2026

@author: Admin
"""


import streamlit as st
import pickle
import numpy as np
import sqlite3
import hashlib
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="MediPredict", layout="wide")


# css

st.markdown("""
<style>

/* Main app background */
.main {
    background-color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e3a8a;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white;
}

/* Titles */
.title {
    color: #1e3a8a;
    font-weight: bold;
}

/* HERO SECTION */
.hero-section {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    padding: 45px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

/* Hero Title */
.hero-title {
    font-size: 55px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Hero Subtitle */
.hero-subtitle {
    font-size: 22px;
    opacity: 0.9;
}

/* Feature Cards */
.info-card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    text-align: center;
    height: 200px;
}

/* Stats Cards */
.stat-card {
    background-color: #eff6ff;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    border-left: 5px solid #3b82f6;
}

.stat-card h2 {
    font-size: 40px;
    color: #1e3a8a;
}

.stat-card p {
    color: #475569;
    font-size: 18px;
}

/* LOGIN PAGE CARD */
.card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #3b82f6;
    margin-bottom: 25px;
}

/* INPUT FIELDS */
.stTextInput input{
    border-radius:12px;
    border:2px solid #dbeafe;
    padding:12px;
    background:#f8fafc;
}

/* BUTTONS */
.stButton>button{
    background:linear-gradient(90deg,#1e3a8a,#3b82f6);
    color:white;
    border:none;
    border-radius:12px;
    height:3em;
    font-size:18px;
    font-weight:bold;
    transition:0.3s;
}

/* BUTTON HOVER */
.stButton>button:hover{
    transform:scale(1.02);
    background:linear-gradient(90deg,#2563eb,#60a5fa);
    color:white;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        disease TEXT,
        result TEXT,
        date TEXT
    )
    '''
)

conn.commit()

# =====================================================
# PASSWORD HASHING
# =====================================================


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================================
# SESSION
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# ===================================================== 
# AUTH FUNCTIONS
# =====================================================

def register_user(username, password):

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )

        conn.commit()
        return True

    except:
        return False


def login_user(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    return cursor.fetchone()
def auth_page():
    
    # CUSTOM CSS
    st.markdown("""
    <style>
    .stButton > button {
        height: 45px;
        font-size: 16px;
        border-radius: 10px;
    }

    .stTextInput input {
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
    <div style='
        background: linear-gradient(90deg,#1e3a8a,#3b82f6);
        padding:12px;
        border-radius:14px;
        text-align:center;
        color:white;
        margin-bottom:20px;
        width:45%;
        margin-left:auto;
        margin-right:auto;
        box-shadow:0 4px 12px rgba(0,0,0,0.12);
    '>
    
    <h1 style='
        font-size:26px;
        margin-bottom:5px;
        color:white;
    '>
    ☤ MediPredict
    </h1>
    
    <p style='
        font-size:14px;
        margin:0;
        color:white;
    '>
    AI Powered Multiple Disease Prediction System
    </p>
    
    </div>
    """, unsafe_allow_html=True)
    
    

    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # =====================================================
    # LOGIN
    # =====================================================
    with tab1:
        
            st.markdown("""
            <h1 style="
                text-align:center;
                color:#1e3a8a;
                font-size:42px;
                margin-top:10px;
                margin-bottom:0px;
            ">
                Welcome Back
            </h1>
            
            <p style="
                text-align:center;
                color:gray;
                font-size:18px;
                margin-bottom:30px;
            ">
                Login to continue
            </p>
            """, unsafe_allow_html=True)
        
            col1, col2, col3 = st.columns([1.5,2,1.5])
        
            with col2:
        
                username = st.text_input("👤 Username")
                password = st.text_input("🔒 Password", type="password")
        
                if st.button("Login", use_container_width=True):
        
                    user = login_user(username, password)
        
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login Successful")
                        st.rerun()
        
                    else:
                        st.error("Invalid Username or Password")
    # =====================================================
    # REGISTER
    # =====================================================
    with tab2:
    
        col1, col2, col3 = st.columns([1.5,2,1.5])
    
        with col2:

            st.markdown("""
            <h1 style='
                text-align:center;
                color:#1e3a8a;
                font-size:42px;
                margin-top:10px;
                margin-bottom:0px;
            '>
            Create Account
            </h1>
            
            <p style='
                text-align:center;
                color:gray;
                font-size:18px;
                margin-bottom:30px;
            '>
            Register to get started
            </p>
            """, unsafe_allow_html=True)

            new_user = st.text_input("👤 Create Username")
        
            new_password = st.text_input(
                "🔒 Create Password",
                type="password"
            )
    
    
            st.markdown("<br>", unsafe_allow_html=True)
    
            if st.button("Register", use_container_width=True):
    
                if new_user == "" or new_password == "":
                    st.warning("Please fill all fields")
    
                else:
                    success = register_user(new_user, new_password)
    
                    if success:
                        st.success("Account Created Successfully")
    
                    else:
                        st.error("Username already exists")
# =====================================================
# SHOW LOGIN PAGE FIRST
# =====================================================

if not st.session_state.logged_in:
    auth_page()
    st.stop()  
    
st.title("Multiple Disease Prediction System")
# =====================================================
# LOAD MODELS
# =====================================================

@st.cache_resource

def load_models():

    diabetes_model = pickle.load(open("saved_model/diabetes_model.sav", "rb"))
    diabetes_scaler = pickle.load(open("saved_model/diabetes_scaler.sav", "rb"))
    
    heart_model = pickle.load(open("saved_model/heart_model.sav", "rb"))
    heart_scaler = pickle.load(open("saved_model/heart_scaler.sav", "rb"))

    parkinsons_model = pickle.load(open("saved_model/parkinsons_model.sav", "rb"))
    parkinsons_scaler = pickle.load(open("saved_model/parkinsons_scaler.sav", "rb"))
    

    return (
        diabetes_model,
        diabetes_scaler,
        heart_model,
        heart_scaler,
        parkinsons_model,
        parkinsons_scaler
    )

(
    diabetes_model,
    diabetes_scaler,
    heart_model,
    heart_scaler,
    parkinsons_model,
    parkinsons_scaler
) = load_models()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    
    st.success(f"Logged in as {st.session_state.username}")

    selected = option_menu(
    "MediPredict",
    [
        "Home",
        "Diabetes Prediction",
        "Heart Disease Prediction",
        "Parkinsons Prediction",
        "Prediction History"
    ],
    icons=[
        'house',
        'activity',
        'heart',
        'person',
        'clock-history'
    ],
    default_index=0,

    styles={
        "container": {
            "padding": "5!important",
            "background-color": "#ffffff"
        },

        "icon": {
            "color": "#1e293b",
            "font-size": "18px"
        },

        "nav-link": {
            "font-size": "18px",
            "text-align": "left",
            "margin": "5px",
            "color": "#1e293b",
            "--hover-color": "#e5e7eb",
        },

        "nav-link-selected": {
            "background-color": "#9ca3af",
            "color": "white",
        },
    }
)
# Logout Button
    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()   


# =========================================================
# HOME PAGE
# =========================================================

if selected == "Home":

    # HERO SECTION
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">
    <span style="color:white; font-size:65px;">⚕</span> MediPredict
</h1>
        <p class="hero-subtitle">
              Predict.  Prevent.  Stay Healthy
        </p>
    </div>
    """, unsafe_allow_html=True)

    # FEATURE CARDS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>Diabetes</h3>
            <p>Predict diabetes risk using intelligent AI analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>Heart Disease</h3>
            <p>Analyze heart health and cardiovascular risks.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>Parkinson's</h3>
            <p>Early Parkinson's detection using machine learning.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # STATS SECTION
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("""
        <div class="stat-card">
            <h2>3+</h2>
            <p>Diseases Supported</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="stat-card">
            <h2>95%</h2>
            <p>Prediction Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="stat-card">
            <h2>24/7</h2>
            <p>System Status</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    

# =====================================================
# SAVE HISTORY
# =====================================================


def save_history(disease, result):

    cursor.execute(
        "INSERT INTO history (username, disease, result, date) VALUES (?, ?, ?, ?)",
        (
            st.session_state.username,
            disease,
            result,
            str(datetime.now())
        )
    )

    conn.commit()

# =====================================================
# DIABETES
# =====================================================

if selected == 'Diabetes Prediction':

    st.header('Diabetes Prediction')

    col1, col2 = st.columns(2)

    with col1:
        pregnancies = st.number_input('Pregnancies', min_value=0.0)
        glucose = st.number_input('Glucose Level')
        bloodpressure = st.number_input('Blood Pressure')
        skinthickness = st.number_input('Skin Thickness')

    with col2:
        insulin = st.number_input('Insulin Level')
        bmi = st.number_input('BMI Value')
        diabetespedigreefunction = st.number_input('Diabetes Pedigree Function')
        age = st.number_input('Age')

    if st.button('Predict Diabetes'):
        if (pregnancies == 0 and glucose == 0 and bloodpressure == 0 and
        skinthickness == 0 and insulin == 0 and bmi == 0 and
        diabetespedigreefunction == 0 and age == 0):

            st.warning("Please enter patient details first")

        else:
            input_data = np.array([[pregnancies, glucose, bloodpressure,
                                    skinthickness, insulin, bmi,
                                    diabetespedigreefunction, age]])
    
            input_data = diabetes_scaler.transform(input_data)
    
            prediction = diabetes_model.predict(input_data)
            probability = diabetes_model.predict_proba(input_data)
    
            risk = round(probability[0][1] * 100, 2)
    
            st.progress(int(risk))
            st.info(f"Diabetes Risk Score: {risk}%")
    
            if prediction[0] == 1:
                result = 'High Risk of Diabetes'
                st.error(result)
            else:
                result = 'Low Risk of Diabetes'
                st.success(result)
    
            save_history("Diabetes", result)
    
            chart = pd.DataFrame({
                'Category': ['Risk', 'Safe'],
                'Value': [risk, 100-risk]
            })
    
            fig = px.pie(chart, names='Category', values='Value', title='Diabetes Risk Analysis')
            st.plotly_chart(fig, width= 'stretch')

# =====================================================
# HEART DISEASE
# =====================================================
elif selected == 'Heart Disease Prediction':

    st.header('Heart Disease Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age')
        trestbps = st.number_input('Resting Blood Pressure')
        restecg = st.number_input('Resting ECG')
        oldpeak = st.number_input('Oldpeak')
        thal = st.number_input('Thal')

    with col2:
        sex = st.number_input('Sex')
        chol = st.number_input('Serum Cholesterol')
        thalach = st.number_input('Maximum Heart Rate')
        slope = st.number_input('Slope')

    with col3:
        cp = st.number_input('Chest Pain Type')
        fbs = st.number_input('Fasting Blood Sugar')
        exang = st.number_input('Exercise Induced Angina')
        ca = st.number_input('Major Vessels')

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button('Predict Heart Disease'):
        
        if (age == 0 and sex == 0 and cp == 0 and trestbps == 0 and
            chol == 0 and fbs == 0 and restecg == 0 and
            thalach == 0 and exang == 0 and oldpeak == 0 and
            slope == 0 and ca == 0 and thal == 0):
    
            st.warning("Please enter patient details first")

        else:


            input_data = np.array([[age, sex, cp, trestbps,
                                    chol, fbs, restecg,
                                    thalach, exang, oldpeak,
                                    slope, ca, thal]])
    
            input_data = heart_scaler.transform(input_data)
    
            prediction = heart_model.predict(input_data)
            probability = heart_model.predict_proba(input_data)
    
            risk = round(probability[0][1] * 100, 2)
    
            st.progress(int(risk))
            st.info(f"Heart Disease Risk Score: {risk}%")
    
            if prediction[0] == 1:
                result = 'High Risk of Heart Disease'
                st.error(result)
            else:
                result = 'Low Risk of Heart Disease'
                st.success(result)
    
            save_history("Heart Disease", result)
    
            chart = pd.DataFrame({
                'Category': ['Risk', 'Safe'],
                'Value': [risk, 100-risk]
            })
    
            fig = px.pie(
                chart,
                names='Category',
                values='Value',
                title='Heart Disease Risk Analysis'
            )
    
            st.plotly_chart(fig, width='stretch')

# =====================================================
# PARKINSONS
# =====================================================

elif selected == 'Parkinsons Prediction':

    st.header("Parkinson's Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        fo = st.number_input('MDVP:Fo(Hz)')
        fhi = st.number_input('MDVP:Fhi(Hz)')
        flo = st.number_input('MDVP:Flo(Hz)')
        jitter_percent = st.number_input('MDVP:Jitter(%)')
        jitter_abs = st.number_input('MDVP:Jitter(Abs)')
        rap = st.number_input('MDVP:RAP')
        ppq = st.number_input('MDVP:PPQ')
        ddp = st.number_input('Jitter:DDP')

    with col2:
        shimmer = st.number_input('MDVP:Shimmer')
        shimmer_db = st.number_input('MDVP:Shimmer(dB)')
        apq3 = st.number_input('Shimmer:APQ3')
        apq5 = st.number_input('Shimmer:APQ5')
        apq = st.number_input('MDVP:APQ')
        dda = st.number_input('Shimmer:DDA')
        nhr = st.number_input('NHR')
        hnr = st.number_input('HNR')

    with col3:
        rpde = st.number_input('RPDE')
        dfa = st.number_input('DFA')
        spread1 = st.number_input('spread1')
        spread2 = st.number_input('spread2')
        d2 = st.number_input('D2')
        ppe = st.number_input('PPE')

    if st.button('Predict Parkinsons Disease'):
        
        if all(v == 0 for v in [
            fo, fhi, flo, jitter_percent, jitter_abs,
            rap, ppq, ddp, shimmer, shimmer_db,
            apq3, apq5, apq, dda, nhr, hnr,
            rpde, dfa, spread1, spread2, d2, ppe
        ]):
            st.warning("Please enter patient details first")
        else:
            input_data = np.array([[fo, fhi, flo,
                                    jitter_percent, jitter_abs,
                                    rap, ppq, ddp,
                                    shimmer, shimmer_db, apq3,
                                    apq5, apq, dda,
                                    nhr, hnr, rpde,
                                    dfa, spread1, spread2,
                                    d2, ppe]])
    
            input_data = parkinsons_scaler.transform(input_data)
    
            prediction = parkinsons_model.predict(input_data)

            probability = parkinsons_model.predict_proba(input_data)
    
            risk = round(probability[0][1] * 100, 2)
    
            st.progress(int(risk))
            st.info(f"Parkinson's Risk Score: {risk}%")
    
            if prediction[0] == 1:
                result = 'High Risk of Parkinsons Disease'
                st.error(result)
            else:
                result = 'Low Risk of Parkinsons Disease'
                st.success(result)
    
            save_history("Parkinsons", result)
            

            chart = pd.DataFrame({
                'Category': ['Risk', 'Safe'],
                'Value': [risk, 100-risk]
            })
            
            fig = px.pie(
                chart,
                names='Category',
                values='Value',
                title='Predict Parkinsons Disease'
            )
            
            st.plotly_chart(fig, width='stretch')
# =====================================================
# HISTORY
# =====================================================

elif selected == "Prediction History":

    st.header("Prediction History")

    query = pd.read_sql_query(
    "SELECT * FROM history WHERE username=?",
    conn,
    params=(st.session_state.username,)
)

    if query.empty:
        st.warning("No prediction history found")

    else:
        st.dataframe(query)

