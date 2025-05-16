import streamlit as st
import hashlib
import base64
import os
import pandas as pd
import numpy as np

def initialize_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "auth_attempts" not in st.session_state:
        st.session_state.auth_attempts = 0
        
    # Chat related session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "current_survey_responses" not in st.session_state:
        st.session_state.current_survey_responses = {}

def admin_login():
    """Handle admin login functionality"""
    st.subheader("Admin Login")
    
    # Simple authentication - in a real app, use proper authentication
    # For demo purposes, we're using a hardcoded password hash
    # In production, get credentials from environment variables/database
    admin_username = "admin"
    # Password: hurdl2023
    admin_password_hash = "5f4dcc3b5aa765d61d8327deb882cf99"  
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == admin_username and check_password(password, admin_password_hash):
            st.session_state.authenticated = True
            st.session_state.auth_attempts = 0
            st.success("Login successful!")
            st.rerun()
        else:
            st.session_state.auth_attempts += 1
            st.error(f"Invalid credentials. Attempt {st.session_state.auth_attempts} of 5.")
            
            if st.session_state.auth_attempts >= 5:
                st.error("Too many failed attempts. Please try again later.")
                st.session_state.auth_attempts = 0

def check_password(password, stored_hash):
    """Check if password matches stored hash"""
    # In this simple example we use MD5, but in production use a more secure algorithm
    # like bcrypt or Argon2
    password_hash = hashlib.md5(password.encode()).hexdigest()
    return password_hash == stored_hash

def get_color_scale(values, colorscale='RdYlGn'):
    """Get colors from a scale based on values"""
    if colorscale == 'RdYlGn':
        # Red (low) to Green (high)
        return ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']
    elif colorscale == 'YlOrRd':
        # Yellow (low) to Red (high)
        return ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026']
    else:
        # Default blues
        return ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']

def generate_demo_data():
    """Generate sample data for testing"""
    # NOTE: This function is only used for development/testing
    # In the real app, we only use actual user data
    
    departments = ["Engineering", "Marketing", "Sales", "Product", "HR", "Finance"]
    locations = ["Remote", "HQ", "Regional Office"]
    
    # Generate 50 sample responses
    data = []
    for i in range(50):
        response = {
            "response_id": f"test-{i}",
            "timestamp": pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30)),
            "department": np.random.choice(departments),
            "location": np.random.choice(locations)
        }
        
        # Generate answers for 10 questions
        for j in range(1, 11):
            if j <= 8:  # Scale questions
                response[f"q_{j}"] = np.random.randint(1, 6)
            else:  # Text questions
                sentiments = [
                    "I'm feeling great about our team's progress.",
                    "There's too much work and not enough time.",
                    "My manager has been very supportive.",
                    "I'm concerned about the project timeline.",
                    "The workplace environment is positive and productive.",
                    "Communication could be improved in our team."
                ]
                response[f"q_{j}"] = np.random.choice(sentiments)
                
        data.append(response)
    
    return pd.DataFrame(data)
