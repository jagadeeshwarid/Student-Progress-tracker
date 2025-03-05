import streamlit as st
import json
import os
import data_manager  
import auth  
import plotly.express as px
from visualization import create_progress_chart, create_average_progress_chart
from styles import apply_custom_styles

# File for storing completion dates
COMPLETION_DATE_FILE = "completion_dates.json"

# Initialize Data
manager = data_manager.DataManager()
auth_instance = auth.Auth(manager)
apply_custom_styles()

# Function to Load Completion Dates from JSON
def load_completion_dates():
    if os.path.exists(COMPLETION_DATE_FILE):
        try:
            with open(COMPLETION_DATE_FILE, "r") as f:
                data = f.read().strip()
                return json.loads(data) if data else {}  # Empty JSON if file is empty
        except json.JSONDecodeError:
            return {}  # Return empty dictionary if JSON is corrupt
    return {}

# Function to Save Completion Dates to JSON
def save_completion_dates(data):
    temp_file = COMPLETION_DATE_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(temp_file, COMPLETION_DATE_FILE)  # Safely replace original file

# Load saved completion dates
completion_dates = load_completion_dates()

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.update({
        "logged_in": False,
        "username": None,
        "role": None,
        "current_page": "login",
        "selected_track": None,
        "selected_phase": None,
        "selected_topic": None
    })

# Display Logo
if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=700)

# Main Title
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📊 ProITbridge Milestone Tracker</h1>", unsafe_allow_html=True)

# Authentication
if not st.session_state["logged_in"]:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login Page", use_container_width=True, type="primary" if st.session_state["current_page"] == "login" else "secondary"):
            st.session_state["current_page"] = "login"
            st.rerun()
    with col2:
        if st.button("Register Page", use_container_width=True, type="primary" if st.session_state["current_page"] == "register" else "secondary"):
            st.session_state["current_page"] = "register"
            st.rerun()

    if st.session_state["current_page"] == "login":
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        st.selectbox("Role", ["student", "admin"], key="login_role")

        if st.button("🔐 Login", key="login_button"):
            username = st.session_state.get("login_username", "")
            password = st.session_state.get("login_password", "")
            role = st.session_state.get("login_role", "student")

            if username and password:
                if auth_instance.login(username, password, role):
                    st.session_state.update({
                        "logged_in": True,
                        "username": username,
                        "role": role,
                        "authentication_status": True
                    })
                    st.rerun()
    else:
        st.text_input("Username", key="register_username")
        st.text_input("Password", type="password", key="register_password")
        st.text_input("Confirm Password", type="password", key="register_password_confirm")

        if st.button("📝 Register", key="register_button"):
            if st.session_state["register_password"] != st.session_state["register_password_confirm"]:
                st.error("Passwords do not match!")
            else:
                username = st.session_state.get("register_username", "")
                password = st.session_state.get("register_password", "")

                if username and password:
                    if auth_instance.register(username, password):
                        st.session_state["register_status"] = "success"
                        st.session_state["current_page"] = "login"
                        st.rerun()
                    else:
                        st.session_state["register_status"] = "error"
else:
    with st.sidebar:
        st.write(f"👤 Welcome, {st.session_state['username']}!")
        st.write(f"Role: {st.session_state['role'].capitalize()}")
        if st.button("Logout", use_container_width=True):
            auth_instance.logout()
            st.rerun()

    # Career Path Selection
    st.markdown("## 🎯 Select Your Career Path")
    selected_track = st.selectbox("Choose a Track", ["Data Analyst", "Data Scientist"], index=None, placeholder="Select a Career Path")

    if selected_track:
        topics_data = manager.get_topics(selected_track)

        # Phase Selection
        selected_phase = st.selectbox("Select a Phase", list(topics_data.keys()), index=None, placeholder="Select a Phase")

        if selected_phase:
            topics = topics_data[selected_phase]
            
            # Topic Selection
            selected_topic = st.selectbox("Select a Topic", list(topics.keys()), index=None, placeholder="Select a Topic")

            if selected_topic:
                subtopics = topics[selected_topic]
                progress_data = {}

                st.markdown(f"### 📌 Select and Rate Progress for *{selected_topic}*")

                if isinstance(subtopics, list):
                    for subtopic in subtopics:
                        col1, col2, col3 = st.columns([3, 1, 2])

                        with col1:
                            checked = st.checkbox(subtopic, value=completion_dates.get(subtopic, {}).get("progress", False))

                        with col2:
                            percentage = st.slider("", 0, 100, completion_dates.get(subtopic, {}).get("progress", 0), key=subtopic)
                            progress_data[subtopic] = percentage

                        # Completion Date Handling
                        with col3:
                            prev_dates = completion_dates.get(subtopic, {}).get("dates", [])  # Load previous dates (list)

                            # Show latest date in the input (or empty initially)
                            current_date = st.date_input("Completion Date", value=None if not prev_dates else prev_dates[-1], key=f"date_{subtopic}")

                            if current_date:
                                if not prev_dates or prev_dates[-1] != current_date:  # Update only if new date is different
                                    prev_dates.append(str(current_date))  # Append new date as a string
                                    completion_dates[subtopic] = {"dates": prev_dates, "progress": percentage}

                            # Display previous dates with strikethrough for old ones
                            if prev_dates:
                                formatted_dates = "  ".join([f"~~{d}~~" for d in prev_dates[:-1]])  # Slash old dates
                                formatted_dates += f"  ➡  **{prev_dates[-1]}**"  # Show latest date bold
                                st.markdown(formatted_dates)

                # Save Updated Dates
                save_completion_dates(completion_dates)

                # Generate Phase-Wise Pie Chart
                if progress_data:
                    fig_phase = px.pie(names=list(progress_data.keys()), values=list(progress_data.values()), title=f"{selected_phase} Progress")
                    st.plotly_chart(fig_phase)

                    # Calculate Overall Progress
                    overall_progress = {}
                    for phase, topics in topics_data.items():
                        phase_progress = []
                        for topic, subtopics in topics.items():
                            if isinstance(subtopics, list):
                                phase_progress.extend([completion_dates.get(sub, {}).get("progress", 0) for sub in subtopics])

                        if phase_progress:
                            overall_progress[phase] = sum(phase_progress) / len(phase_progress)

                    # Generate Overall Progress Pie Chart
                    if overall_progress:
                        fig_overall = px.pie(names=list(overall_progress.keys()), values=list(overall_progress.values()), title=f"Overall {selected_track} Progress")
                        st.plotly_chart(fig_overall)

    # Admin View: Monitor Student Progress
    if st.session_state["role"] == "admin":
        st.markdown("## 📈 Students' Progress Overview")
        create_average_progress_chart()
