import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_wellbeing_chart(df):
    """Render the wellbeing index chart"""
    st.subheader("Wellbeing Index Trends")
    
    # Ensure we have timestamp column
    if 'timestamp' not in df.columns:
        st.warning("No timestamp data available for trend visualization.")
        return
    
    # Get wellbeing questions
    wellbeing_questions = ["q_1", "q_2", "q_3", "q_4"]
    available_questions = [q for q in wellbeing_questions if q in df.columns]
    
    if not available_questions:
        st.warning("No wellbeing data available for visualization.")
        return
    
    # Calculate wellbeing score for each response
    df['wellbeing_score'] = df[available_questions].mean(axis=1)
    
    # Group by date
    df['date'] = df['timestamp'].dt.date
    daily_wellbeing = df.groupby('date')['wellbeing_score'].mean().reset_index()
    daily_wellbeing['date'] = pd.to_datetime(daily_wellbeing['date'])
    
    # Create department breakdown
    dept_wellbeing = df.groupby(['department', 'date'])['wellbeing_score'].mean().reset_index()
    dept_wellbeing['date'] = pd.to_datetime(dept_wellbeing['date'])
    
    # Create overall trend chart
    trend_chart = alt.Chart(daily_wellbeing).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('wellbeing_score:Q', scale=alt.Scale(domain=[1, 5]), title='Wellbeing Score'),
        tooltip=['date:T', 'wellbeing_score:Q']
    ).properties(
        title='Overall Wellbeing Score Trend',
        width='container',
        height=300
    )
    
    st.altair_chart(trend_chart, use_container_width=True)
    
    # Create department comparison chart
    if len(df['department'].unique()) > 1:
        st.subheader("Wellbeing by Department")
        
        dept_chart = alt.Chart(dept_wellbeing).mark_line().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('wellbeing_score:Q', scale=alt.Scale(domain=[1, 5]), title='Wellbeing Score'),
            color=alt.Color('department:N', title='Department'),
            tooltip=['date:T', 'department:N', 'wellbeing_score:Q']
        ).properties(
            width='container',
            height=300
        )
        
        st.altair_chart(dept_chart, use_container_width=True)
    
    # Show individual question breakdown
    st.subheader("Wellbeing Questions Breakdown")
    
    # Calculate average for each question
    question_scores = {}
    for q in available_questions:
        question_scores[q] = df[q].mean()
    
    # Create DataFrame for chart
    question_df = pd.DataFrame({
        'Question': list(question_scores.keys()),
        'Score': list(question_scores.values())
    })
    
    # Map question IDs to more readable names
    question_map = {
        'q_1': 'Overall Wellbeing',
        'q_2': 'Work-Life Balance',
        'q_3': 'Stress Level',
        'q_4': 'Job Satisfaction'
    }
    
    question_df['Question'] = question_df['Question'].map(lambda q: question_map.get(q, q))
    
    # Create bar chart
    bar_chart = alt.Chart(question_df).mark_bar().encode(
        x=alt.X('Score:Q', scale=alt.Scale(domain=[1, 5])),
        y=alt.Y('Question:N', sort='-x'),
        color=alt.Color('Score:Q', scale=alt.Scale(domain=[1, 5], scheme='redyellowgreen')),
        tooltip=['Question:N', 'Score:Q']
    ).properties(
        width='container',
        height=200
    )
    
    st.altair_chart(bar_chart, use_container_width=True)

def render_safety_chart(df):
    """Render the psychological safety chart"""
    st.subheader("Psychological Safety Analysis")
    
    # Ensure we have timestamp column
    if 'timestamp' not in df.columns:
        st.warning("No timestamp data available for trend visualization.")
        return
    
    # Get safety questions
    safety_questions = ["q_5", "q_6", "q_7", "q_8"]
    available_questions = [q for q in safety_questions if q in df.columns]
    
    if not available_questions:
        st.warning("No psychological safety data available for visualization.")
        return
    
    # Calculate safety score for each response
    df['safety_score'] = df[available_questions].mean(axis=1)
    
    # Group by date
    df['date'] = df['timestamp'].dt.date
    daily_safety = df.groupby('date')['safety_score'].mean().reset_index()
    daily_safety['date'] = pd.to_datetime(daily_safety['date'])
    
    # Create overall trend chart
    trend_chart = alt.Chart(daily_safety).mark_line(point=True).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('safety_score:Q', scale=alt.Scale(domain=[1, 5]), title='Safety Score'),
        tooltip=['date:T', 'safety_score:Q']
    ).properties(
        title='Psychological Safety Score Trend',
        width='container',
        height=300
    )
    
    st.altair_chart(trend_chart, use_container_width=True)
    
    # Show individual question breakdown
    st.subheader("Psychological Safety Questions Breakdown")
    
    # Calculate average for each question
    question_scores = {}
    for q in available_questions:
        question_scores[q] = df[q].mean()
    
    # Create DataFrame for chart
    question_df = pd.DataFrame({
        'Question': list(question_scores.keys()),
        'Score': list(question_scores.values())
    })
    
    # Map question IDs to more readable names
    question_map = {
        'q_5': 'Team Psychological Safety',
        'q_6': 'Speaking Up Comfort',
        'q_7': 'Management Support',
        'q_8': 'Mistake Tolerance'
    }
    
    question_df['Question'] = question_df['Question'].map(lambda q: question_map.get(q, q))
    
    # Create bar chart
    bar_chart = alt.Chart(question_df).mark_bar().encode(
        x=alt.X('Score:Q', scale=alt.Scale(domain=[1, 5])),
        y=alt.Y('Question:N', sort='-x'),
        color=alt.Color('Score:Q', scale=alt.Scale(domain=[1, 5], scheme='redyellowgreen')),
        tooltip=['Question:N', 'Score:Q']
    ).properties(
        width='container',
        height=200
    )
    
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Department comparison
    if len(df['department'].unique()) > 1:
        st.subheader("Psychological Safety by Department")
        
        dept_safety = df.groupby('department')['safety_score'].mean().reset_index()
        dept_safety = dept_safety.sort_values('safety_score', ascending=False)
        
        dept_chart = alt.Chart(dept_safety).mark_bar().encode(
            x=alt.X('safety_score:Q', scale=alt.Scale(domain=[1, 5]), title='Safety Score'),
            y=alt.Y('department:N', sort='-x', title='Department'),
            color=alt.Color('safety_score:Q', scale=alt.Scale(domain=[1, 5], scheme='redyellowgreen')),
            tooltip=['department:N', 'safety_score:Q']
        ).properties(
            width='container',
            height=250
        )
        
        st.altair_chart(dept_chart, use_container_width=True)

def render_workload_heatmap(df, workload_scores):
    """Render the workload heatmap"""
    st.subheader("Workload Heatmap")
    
    # Check if workload data is available
    if workload_scores["by_department"].empty:
        st.warning("No workload data available for visualization.")
        return
    
    # Combine department and location data
    combined_data = pd.concat([workload_scores["by_department"], workload_scores["by_location"]])
    
    # Create a uniform color scale for score
    # Reverse color scale (high workload is red)
    fig = px.density_heatmap(
        combined_data, 
        x="type", 
        y="category", 
        z="score",
        color_continuous_scale="RdYlGn_r",  # Red for high workload, green for low
        range_color=[1, 5],
        title="Workload Distribution by Department and Location"
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        width=700,
        height=400,
        margin=dict(l=40, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional workload analysis - time trend
    if 'timestamp' in df.columns:
        st.subheader("Workload Trend Over Time")
        
        # Get workload questions
        workload_questions = ["q_3", "q_7"]
        available_questions = [q for q in workload_questions if q in df.columns]
        
        if available_questions:
            # Calculate workload score for each response
            df['workload_score'] = df[available_questions].mean(axis=1)
            
            # Group by date
            df['date'] = df['timestamp'].dt.date
            daily_workload = df.groupby('date')['workload_score'].mean().reset_index()
            daily_workload['date'] = pd.to_datetime(daily_workload['date'])
            
            # Create line chart
            workload_chart = alt.Chart(daily_workload).mark_line(point=True).encode(
                x=alt.X('date:T', title='Date'),
                y=alt.Y('workload_score:Q', scale=alt.Scale(domain=[1, 5]), title='Workload Score'),
                tooltip=['date:T', 'workload_score:Q']
            ).properties(
                width='container',
                height=300
            )
            
            st.altair_chart(workload_chart, use_container_width=True)
            st.caption("Higher workload scores indicate higher perceived workload")

def render_sentiment_chart(df, sentiment_scores):
    """Render the sentiment analysis chart"""
    st.subheader("Sentiment Analysis")
    
    # Check if sentiment data is available
    if sentiment_scores["overall"] == 0:
        st.warning("No sentiment data available for visualization.")
        return
    
    # Display overall sentiment
    st.metric("Overall Sentiment Score", f"{sentiment_scores['overall']:.2f}/5")
    
    # Question-specific sentiment
    if sentiment_scores["questions"]:
        st.subheader("Sentiment by Question")
        
        # Create DataFrame for question sentiments
        question_df = pd.DataFrame({
            'Question': list(sentiment_scores["questions"].keys()),
            'Score': list(sentiment_scores["questions"].values())
        })
        
        # Map question IDs to more readable names
        question_map = {
            'q_9': 'How are you feeling about work?',
            'q_10': 'Any additional feedback?'
        }
        
        question_df['Question'] = question_df['Question'].map(lambda q: question_map.get(q, q))
        
        # Create bar chart
        bar_chart = alt.Chart(question_df).mark_bar().encode(
            x=alt.X('Score:Q', scale=alt.Scale(domain=[1, 5])),
            y=alt.Y('Question:N', sort='-x'),
            color=alt.Color('Score:Q', scale=alt.Scale(domain=[1, 5], scheme='redyellowgreen')),
            tooltip=['Question:N', 'Score:Q']
        ).properties(
            width='container',
            height=150
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
    
    # Common words visualization
    if sentiment_scores["common_words"]:
        st.subheader("Common Words in Feedback")
        
        # Create DataFrame for word counts
        words_df = pd.DataFrame({
            'Word': list(sentiment_scores["common_words"].keys()),
            'Count': list(sentiment_scores["common_words"].values())
        }).sort_values('Count', ascending=False)
        
        # Create bar chart
        word_chart = alt.Chart(words_df).mark_bar().encode(
            x=alt.X('Count:Q'),
            y=alt.Y('Word:N', sort='-x'),
            tooltip=['Word:N', 'Count:Q']
        ).properties(
            width='container',
            height=300
        )
        
        st.altair_chart(word_chart, use_container_width=True)
    
    # Topic analysis
    if sentiment_scores["topics"]:
        st.subheader("Common Topics in Feedback")
        
        # Create DataFrame for topics
        topics_df = pd.DataFrame({
            'Topic': list(sentiment_scores["topics"].keys()),
            'Mentions': list(sentiment_scores["topics"].values())
        }).sort_values('Mentions', ascending=False)
        
        # Create bar chart
        topic_chart = alt.Chart(topics_df).mark_bar().encode(
            x=alt.X('Mentions:Q'),
            y=alt.Y('Topic:N', sort='-x'),
            tooltip=['Topic:N', 'Mentions:Q']
        ).properties(
            width='container',
            height=200
        )
        
        st.altair_chart(topic_chart, use_container_width=True)

def render_trend_alerts(trends):
    """Render trend alerts"""
    st.subheader("Trend Alerts")
    
    if not trends:
        st.info("No significant trends detected in the current period.")
        return
    
    # Create columns for the alerts
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.write("**Metric**")
    with col2:
        st.write("**Change**")
    
    # Display each trend
    for trend in trends:
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.write(f"**{trend['metric']}**")
            
            with col2:
                # Format the trend display
                if trend['direction'] == 'up':
                    if 'wellbeing' in trend['metric'].lower() or 'safety' in trend['metric'].lower() or 'sentiment' in trend['metric'].lower():
                        # For these metrics, up is good
                        color = "green"
                        icon = "📈"
                    else:
                        # For workload, up might be bad
                        color = "red"
                        icon = "⚠️"
                else:
                    if 'wellbeing' in trend['metric'].lower() or 'safety' in trend['metric'].lower() or 'sentiment' in trend['metric'].lower():
                        # For these metrics, down is bad
                        color = "red"
                        icon = "📉"
                    else:
                        # For workload, down might be good
                        color = "green"
                        icon = "✅"
                
                # Display the trend
                st.markdown(
                    f"<span style='color:{color};'>{icon} {trend['direction'].upper()}</span> by "
                    f"{abs(trend['change']):.2f} points "
                    f"({abs(trend['percent_change']):.1f}%)",
                    unsafe_allow_html=True
                )
                
                # Display current and previous values
                st.write(f"Current: {trend['current']:.2f}, Previous: {trend['previous']:.2f}")
                
                # Add department info if available
                if 'department' in trend:
                    st.write(f"Department: {trend['department']}")
                
                # Add severity indicator
                if trend['severity'] == 'high':
                    st.markdown("<span style='color:red;'>High Severity</span>", unsafe_allow_html=True)
