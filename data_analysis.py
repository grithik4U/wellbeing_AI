import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from datetime import datetime, timedelta

def calculate_wellbeing_index(df):
    """
    Calculate overall wellbeing index from survey responses.
    Scale of 1-5, with 5 being the best.
    """
    # Questions related to wellbeing (adjust based on actual questions)
    wellbeing_questions = ["q_1", "q_2", "q_3", "q_4"]
    
    # Check if we have these columns
    available_questions = [q for q in wellbeing_questions if q in df.columns]
    
    if not available_questions:
        return 0
    
    # Calculate average
    wellbeing_scores = df[available_questions].mean(axis=1)
    overall_wellbeing = wellbeing_scores.mean()
    
    return overall_wellbeing

def calculate_psychological_safety(df):
    """
    Calculate psychological safety score from survey responses.
    Scale of 1-5, with 5 being the best.
    """
    # Questions related to psychological safety (adjust based on actual questions)
    safety_questions = ["q_5", "q_6", "q_7", "q_8"]
    
    # Check if we have these columns
    available_questions = [q for q in safety_questions if q in df.columns]
    
    if not available_questions:
        return 0
    
    # Calculate average
    safety_scores = df[available_questions].mean(axis=1)
    overall_safety = safety_scores.mean()
    
    return overall_safety

def analyze_sentiment(df):
    """
    Analyze sentiment from text responses.
    Returns sentiment scores and analysis.
    """
    # Questions with text responses (adjust based on actual questions)
    text_questions = ["q_9", "q_10"]
    
    # Check if we have these columns
    available_questions = [q for q in text_questions if q in df.columns]
    
    if not available_questions:
        return {"overall": 0, "questions": {}, "common_words": {}, "topics": {}}
    
    # Overall sentiment dictionary
    sentiment_results = {
        "overall": 0,
        "questions": {},
        "common_words": {},
        "topics": {}
    }
    
    all_text = []
    
    # Analyze each text question
    for question in available_questions:
        # Get non-empty responses
        responses = df[question].dropna().astype(str)
        responses = responses[responses.str.strip() != ""]
        
        if len(responses) == 0:
            sentiment_results["questions"][question] = 0
            continue
        
        # Calculate sentiment for each response
        sentiments = []
        for response in responses:
            if isinstance(response, str) and response.strip():
                blob = TextBlob(response)
                # Convert from -1 to 1 scale to 1 to 5 scale
                sentiment = (blob.sentiment.polarity + 1) * 2 + 1
                sentiments.append(sentiment)
                all_text.append(response)
        
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            sentiment_results["questions"][question] = avg_sentiment
        else:
            sentiment_results["questions"][question] = 0
    
    # Overall sentiment
    if sentiment_results["questions"]:
        sentiment_results["overall"] = sum(sentiment_results["questions"].values()) / len(sentiment_results["questions"])
    
    # Extract common words and topics
    if all_text:
        # Combine all text
        combined_text = " ".join(all_text).lower()
        
        # Remove common stop words
        stop_words = ["the", "and", "i", "to", "a", "is", "in", "that", "it", "of", "for", "this", "with", "on", "be", "are"]
        words = re.findall(r'\b\w+\b', combined_text)
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Get top 10 words
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        sentiment_results["common_words"] = dict(top_words)
        
        # Identify potential topics based on common words
        topics = {
            "workload": sum(1 for word in words if word in ["work", "workload", "busy", "overwork", "stress", "deadline", "time"]),
            "team": sum(1 for word in words if word in ["team", "colleague", "coworker", "collaboration", "together"]),
            "management": sum(1 for word in words if word in ["manager", "management", "leadership", "supervisor", "boss"]),
            "growth": sum(1 for word in words if word in ["growth", "learning", "development", "progress", "career"])
        }
        
        sentiment_results["topics"] = topics
    
    return sentiment_results

def calculate_workload_scores(df):
    """
    Calculate workload scores by department and location.
    """
    # Questions related to workload (adjust based on actual questions)
    workload_questions = ["q_3", "q_7"]
    
    # Check if we have these columns
    available_questions = [q for q in workload_questions if q in df.columns]
    
    if not available_questions:
        # Return empty results if no workload questions available
        return {
            "by_department": pd.DataFrame(),
            "by_location": pd.DataFrame(),
            "overall": 0
        }
    
    # Calculate average workload score per response
    df['workload_score'] = df[available_questions].mean(axis=1)
    
    # Group by department
    dept_workload = df.groupby('department')['workload_score'].mean().reset_index()
    dept_workload.columns = ['category', 'score']
    dept_workload['type'] = 'department'
    
    # Group by location
    loc_workload = df.groupby('location')['workload_score'].mean().reset_index()
    loc_workload.columns = ['category', 'score']
    loc_workload['type'] = 'location'
    
    # Overall workload
    overall_workload = df['workload_score'].mean()
    
    return {
        "by_department": dept_workload,
        "by_location": loc_workload,
        "overall": overall_workload
    }

def detect_trends(full_df, current_df):
    """
    Detect trends in the data by comparing current period to previous periods.
    Returns alerts and trend information.
    """
    # Ensure we have timestamp column
    if 'timestamp' not in full_df.columns:
        return []
    
    # Get current period start date (from filtered data)
    if len(current_df) > 0:
        current_start = current_df['timestamp'].min()
        current_end = current_df['timestamp'].max()
    else:
        # No data in current period
        return []
    
    # Calculate previous period (same duration as current period)
    period_duration = current_end - current_start
    previous_end = current_start - timedelta(seconds=1)  # Just before current period
    previous_start = previous_end - period_duration
    
    # Filter for previous period
    previous_df = full_df[(full_df['timestamp'] >= previous_start) & 
                          (full_df['timestamp'] <= previous_end)]
    
    # If no previous data, return empty trends
    if len(previous_df) == 0:
        return []
    
    trends = []
    
    # Compare wellbeing index
    current_wellbeing = calculate_wellbeing_index(current_df)
    previous_wellbeing = calculate_wellbeing_index(previous_df)
    
    if abs(current_wellbeing - previous_wellbeing) >= 0.5:  # Significant change threshold
        trends.append({
            "metric": "Wellbeing Index",
            "current": current_wellbeing,
            "previous": previous_wellbeing,
            "change": current_wellbeing - previous_wellbeing,
            "percent_change": (current_wellbeing - previous_wellbeing) / previous_wellbeing * 100 if previous_wellbeing else 0,
            "direction": "up" if current_wellbeing > previous_wellbeing else "down",
            "severity": "high" if abs(current_wellbeing - previous_wellbeing) >= 1.0 else "medium"
        })
    
    # Compare psychological safety
    current_safety = calculate_psychological_safety(current_df)
    previous_safety = calculate_psychological_safety(previous_df)
    
    if abs(current_safety - previous_safety) >= 0.5:  # Significant change threshold
        trends.append({
            "metric": "Psychological Safety",
            "current": current_safety,
            "previous": previous_safety,
            "change": current_safety - previous_safety,
            "percent_change": (current_safety - previous_safety) / previous_safety * 100 if previous_safety else 0,
            "direction": "up" if current_safety > previous_safety else "down",
            "severity": "high" if abs(current_safety - previous_safety) >= 1.0 else "medium"
        })
    
    # Compare sentiment
    current_sentiment = analyze_sentiment(current_df)["overall"]
    previous_sentiment = analyze_sentiment(previous_df)["overall"]
    
    if abs(current_sentiment - previous_sentiment) >= 0.5:  # Significant change threshold
        trends.append({
            "metric": "Sentiment Score",
            "current": current_sentiment,
            "previous": previous_sentiment,
            "change": current_sentiment - previous_sentiment,
            "percent_change": (current_sentiment - previous_sentiment) / previous_sentiment * 100 if previous_sentiment else 0,
            "direction": "up" if current_sentiment > previous_sentiment else "down",
            "severity": "high" if abs(current_sentiment - previous_sentiment) >= 1.0 else "medium"
        })
    
    # Check for department-specific trends
    departments = current_df['department'].unique()
    
    for dept in departments:
        dept_current = current_df[current_df['department'] == dept]
        dept_previous = previous_df[previous_df['department'] == dept]
        
        # Only compare if we have data for both periods
        if len(dept_current) > 0 and len(dept_previous) > 0:
            # Compare wellbeing for this department
            dept_current_wellbeing = calculate_wellbeing_index(dept_current)
            dept_previous_wellbeing = calculate_wellbeing_index(dept_previous)
            
            if abs(dept_current_wellbeing - dept_previous_wellbeing) >= 0.8:  # Higher threshold for department-specific alert
                trends.append({
                    "metric": f"{dept} - Wellbeing",
                    "current": dept_current_wellbeing,
                    "previous": dept_previous_wellbeing,
                    "change": dept_current_wellbeing - dept_previous_wellbeing,
                    "percent_change": (dept_current_wellbeing - dept_previous_wellbeing) / dept_previous_wellbeing * 100 if dept_previous_wellbeing else 0,
                    "direction": "up" if dept_current_wellbeing > dept_previous_wellbeing else "down",
                    "severity": "high" if abs(dept_current_wellbeing - dept_previous_wellbeing) >= 1.5 else "medium",
                    "department": dept
                })
    
    return trends
