import streamlit as st
import pandas as pd
import datetime
import uuid
import os
import time
from utils import initialize_session_state, admin_login, check_password
from survey_questions import get_survey_questions
from data_analysis import (calculate_wellbeing_index, 
                           calculate_psychological_safety, 
                           analyze_sentiment, 
                           detect_trends,
                           calculate_workload_scores)
from visualization import (render_wellbeing_chart, 
                           render_safety_chart, 
                           render_sentiment_chart,
                           render_workload_heatmap,
                           render_trend_alerts)
from database import get_responses, get_filtered_responses, save_response
from ai_assistant import generate_chatbot_response, get_initial_message

# Set page config
st.set_page_config(
    page_title="Hurdl - Workplace Wellbeing Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Create necessary folders
if not os.path.exists("data"):
    try:
        os.makedirs("data")
    except FileExistsError:
        # Directory already exists, which is fine
        pass

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_responses():
    """Load responses from the database"""
    try:
        # Get responses from the database
        return get_responses()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Main application
def main():
    # Sidebar
    with st.sidebar:
        st.title("Hurdl")
        st.subheader("Workplace Wellbeing Platform")
        
        # Navigation
        if st.session_state.authenticated:
            st.sidebar.success("Logged in as Admin")
            if st.sidebar.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()
                
            page = "HR Dashboard"
        else:
            page = st.sidebar.radio("Navigation", ["Employee Check-in", "HR Dashboard"])
            
            if page == "HR Dashboard" and not st.session_state.authenticated:
                st.sidebar.info("Please log in to access the HR Dashboard")
                admin_login()
        
        st.sidebar.image("https://pixabay.com/get/g16b831cd415041e78ecfba9a297568f21cff48e1aeb86dbf89906a21cd975e3c5a83197d60f95b27065b6b75872328c956788bffde50d82a9d5f8107fcf6d5c2_1280.jpg", 
                         caption="Mental Wellbeing", use_container_width=True)
    
    # Main content
    if page == "Employee Check-in":
        render_employee_checkin()
    elif page == "HR Dashboard" and st.session_state.authenticated:
        render_hr_dashboard()
    elif page == "HR Dashboard":
        st.title("HR Dashboard")
        st.info("Please log in using the sidebar to access the HR Dashboard")

def render_employee_checkin():
    st.title("Weekly Wellbeing Check-in")
    st.subheader("Your anonymous feedback helps create a better workplace")
    
    # Basic info (still anonymous)
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox(
            "Department",
            ["Engineering", "Marketing", "Sales", "Product", "HR", "Finance", "Other"]
        )
    
    with col2:
        location = st.selectbox(
            "Location",
            ["Remote", "HQ", "Regional Office", "Other"]
        )
    
    # Show progress
    if "survey_step" not in st.session_state:
        st.session_state.survey_step = 0
    
    # Get questions
    questions = get_survey_questions()
    total_questions = sum(1 for q in questions if q["type"] != "header")
    
    # Display progress
    if st.session_state.survey_step > 0:
        progress_value = min(st.session_state.survey_step / total_questions, 1.0)
        st.progress(progress_value)
        st.write(f"Question {st.session_state.survey_step} of {total_questions}")
    
    # Placeholder for responses
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    
    # Survey form
    with st.form(key="survey_form"):
        # Handle different survey steps
        if st.session_state.survey_step == 0:
            # Intro step
            st.markdown("""
            ### Welcome to your weekly check-in
            
            This quick survey helps us understand how you're feeling at work.
            Your responses are completely anonymous and will help improve our workplace.
            
            It will take less than 3 minutes to complete.
            """)
            
            submit_label = "Start Survey"
        
        elif st.session_state.survey_step > 0 and st.session_state.survey_step <= total_questions:
            # Find current question (accounting for headers)
            current_q_index = 0
            current_q = None
            
            for i, q in enumerate(questions):
                if q["type"] != "header":
                    current_q_index += 1
                
                if current_q_index == st.session_state.survey_step:
                    current_q = q
                    break
                
                # Also display any headers that come before this question
                if q["type"] == "header" and current_q_index == st.session_state.survey_step - 1:
                    st.subheader(q["text"])
            
            # Display the current question
            if current_q:
                if current_q["type"] == "scale":
                    st.write(current_q["text"])
                    response = st.slider("Rating", 1, 5, 3, 
                                        help="1 = Strongly Disagree, 5 = Strongly Agree",
                                        key=f"q_{current_q['id']}")
                    st.session_state.responses[f"q_{current_q['id']}"] = response
                
                elif current_q["type"] == "text":
                    st.write(current_q["text"])
                    response = st.text_area("Response", key=f"q_{current_q['id']}")
                    st.session_state.responses[f"q_{current_q['id']}"] = response
                
                elif current_q["type"] == "radio":
                    st.write(current_q["text"])
                    response = st.radio("Options", current_q["options"], key=f"q_{current_q['id']}")
                    st.session_state.responses[f"q_{current_q['id']}"] = response
            
            if st.session_state.survey_step == total_questions:
                submit_label = "Submit Survey"
            else:
                submit_label = "Next Question"
        
        else:
            # Thank you step
            st.success("Thank you for completing the survey!")
            st.balloons()
            submit_label = "Start New Survey"
            
            # Set flag to show chatbot after form is submitted
            if st.session_state.survey_step == total_questions + 1:
                # Store the survey responses for the chatbot
                st.session_state.current_survey_responses = st.session_state.responses
                
                # Set flag to show chatbot
                st.session_state.show_chatbot = True
        
        # Submit button
        submitted = st.form_submit_button(submit_label)
        
        if submitted:
            if st.session_state.survey_step == 0:
                # Start the survey
                st.session_state.survey_step = 1
                st.rerun()
            
            elif st.session_state.survey_step > 0 and st.session_state.survey_step < total_questions:
                # Move to next question
                st.session_state.survey_step += 1
                st.rerun()
            
            elif st.session_state.survey_step == total_questions:
                # Save responses
                new_response = {
                    "response_id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now(),
                    "department": department,
                    "location": location
                }
                
                # Add all question responses
                for key, value in st.session_state.responses.items():
                    new_response[key] = value
                
                # Save to database
                save_response(new_response)
                
                # Refresh data by invalidating the cache
                # In newer Streamlit versions we'd use st.cache_data.clear()
                # but we'll use rerun to achieve the same effect
                pass
                
                # Reset for thank you message
                st.session_state.survey_step = total_questions + 1
                st.session_state.responses = {}
                st.rerun()
            
            else:
                # Reset to start again
                st.session_state.survey_step = 0
                st.rerun()
    
    # Show chatbot if survey was completed
    if st.session_state.show_chatbot:
        st.subheader("Chat with Hurdl AI Assistant")
        st.write("Our AI assistant is here to chat about your wellbeing and provide support based on your survey responses.")
        
        # Initialize chat if it's empty
        if not st.session_state.chat_messages:
            # Add initial message from AI
            initial_message = get_initial_message(st.session_state.current_survey_responses)
            st.session_state.chat_messages.append({"role": "assistant", "content": initial_message})
        
        # Display chat messages
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant", avatar="🧠").write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # Display user message
            st.chat_message("user").write(prompt)
            
            # Generate response
            with st.spinner("Thinking..."):
                response = generate_chatbot_response(
                    prompt, 
                    st.session_state.current_survey_responses,
                    [m for m in st.session_state.chat_messages if m["role"] != "system"]
                )
            
            # Add AI response to chat history
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            
            # Display AI response
            st.chat_message("assistant", avatar="🧠").write(response)
            
            # Rerun to update the chat display
            st.rerun()
    else:
        # Show some inspirational imagery when chatbot is not shown
        st.image("https://pixabay.com/get/ga933469d2f3c1804571fb9364004d9f1a23479dbb1f9a411723cc1ed6eb9421e63bce3237089010787f794249903b9115cffcf0e1cd289fe55a75a7961316116_1280.jpg", 
                caption="Wellness in the workplace", use_container_width=True)

def render_hr_dashboard():
    st.title("HR Wellbeing Dashboard")
    
    # Load data
    responses_df = load_responses()
    
    if len(responses_df) == 0:
        st.warning("No survey responses available yet. Dashboard will populate once employees complete check-ins.")
        st.image("https://pixabay.com/get/gbb40d0936787ac5d1c9b4679eed711723d4ffe8763556d1456cfebaf3d57293ab0170b4b2b4a3afe48fba98479992e95ed77f6b0ea7161a9c103bf27fe76439a_1280.jpg", 
                 caption="Waiting for data", use_container_width=True)
        return
    
    # Dashboard filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        departments = ["All"] + sorted(responses_df["department"].unique().tolist())
        selected_dept = st.selectbox("Department", departments)
    
    with col2:
        locations = ["All"] + sorted(responses_df["location"].unique().tolist())
        selected_loc = st.selectbox("Location", locations)
    
    with col3:
        # Get min and max date from data
        min_date = responses_df["timestamp"].min().date()
        max_date = responses_df["timestamp"].max().date()
        
        # Default to last 30 days or full range if less
        default_start = max(min_date, (max_date - datetime.timedelta(days=30)))
        
        date_range = st.date_input(
            "Date Range",
            value=(default_start, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            # Adjust end_date to include the entire day
            end_date = datetime.datetime.combine(end_date, datetime.time(23, 59, 59))
        else:
            start_date = min_date
            end_date = datetime.datetime.combine(max_date, datetime.time(23, 59, 59))
    
    # Filter data using database query for better performance
    if selected_dept == "All" and selected_loc == "All":
        # Just filter by date
        filtered_df = get_filtered_responses(
            start_date=datetime.datetime.combine(start_date, datetime.time.min),
            end_date=datetime.datetime.combine(end_date, datetime.time.max)
        )
    else:
        # Filter by all criteria
        filtered_df = get_filtered_responses(
            start_date=datetime.datetime.combine(start_date, datetime.time.min),
            end_date=datetime.datetime.combine(end_date, datetime.time.max),
            department=None if selected_dept == "All" else selected_dept,
            location=None if selected_loc == "All" else selected_loc
        )
    
    if len(filtered_df) == 0:
        st.warning("No data available for the selected filters.")
        return
    
    # Calculate metrics
    wellbeing_index = calculate_wellbeing_index(filtered_df)
    psychological_safety = calculate_psychological_safety(filtered_df)
    sentiment_scores = analyze_sentiment(filtered_df)
    workload_scores = calculate_workload_scores(filtered_df)
    trends = detect_trends(responses_df, filtered_df)
    
    # Display metrics
    st.header("Key Metrics")
    
    # Top metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("Wellbeing Index", f"{wellbeing_index:.1f}/5.0")
    
    with metric_col2:
        st.metric("Psychological Safety", f"{psychological_safety:.1f}/5.0")
    
    with metric_col3:
        st.metric("Sentiment Score", f"{sentiment_scores['overall']:.1f}/5.0")
    
    # Visualizations
    st.header("Detailed Analysis")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Wellbeing Index", 
        "Psychological Safety",
        "Workload Heatmap",
        "Sentiment Analysis",
        "Trend Alerts"
    ])
    
    with tab1:
        render_wellbeing_chart(filtered_df)
        
    with tab2:
        render_safety_chart(filtered_df)
        
    with tab3:
        render_workload_heatmap(filtered_df, workload_scores)
        
    with tab4:
        render_sentiment_chart(filtered_df, sentiment_scores)
        
    with tab5:
        render_trend_alerts(trends)
    
    # Response summary
    st.header("Response Summary")
    st.write(f"Total Responses: {len(filtered_df)}")
    
    # Show by department and location
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Responses by Department")
        dept_counts = filtered_df["department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        st.bar_chart(dept_counts.set_index("Department"))
    
    with col2:
        st.subheader("Responses by Location")
        loc_counts = filtered_df["location"].value_counts().reset_index()
        loc_counts.columns = ["Location", "Count"]
        st.bar_chart(loc_counts.set_index("Location"))
    
    # Show data visualization imagery
    st.image("https://pixabay.com/get/gb369b38f76e80fa3e95a65e4234affee5345ae73597efc76d0fba8fabb58e1c949584e77b86a5460ccdd5fc1f6bea46cb16b9630d5eaf4d48c3b5847a45ebbdc_1280.jpg", 
             caption="Data visualization", use_container_width=True)

if __name__ == "__main__":
    main()
