import os
import openai
from openai import OpenAI
import streamlit as st
import json
from database import get_responses

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_chatbot_response(user_input, survey_responses=None, chat_history=None):
    """
    Generates a response from the AI chatbot based on user input and survey responses.
    
    Args:
        user_input (str): The user's message
        survey_responses (dict): Dictionary containing the user's survey responses
        chat_history (list): List of previous chat messages
    
    Returns:
        str: The AI's response
    """
    
    if chat_history is None:
        chat_history = []
    
    # Prepare the system message with context from survey responses
    system_message = "You are an empathetic wellbeing assistant named Hurdl, dedicated to supporting workplace mental health. "
    
    if survey_responses:
        # Add survey data to the system message
        system_message += "Based on the user's survey responses, I can see: "
        
        wellbeing_score = 0
        stress_level = 0
        work_life_balance = 0
        count = 0
        
        # Process numerical responses
        for key, value in survey_responses.items():
            if key == 'q_1' and isinstance(value, (int, float)):
                system_message += f"Their overall wellbeing is rated {value}/5. "
                wellbeing_score = value
                count += 1
            elif key == 'q_2' and isinstance(value, (int, float)):
                system_message += f"Their work-life balance is rated {value}/5. "
                work_life_balance = value
                count += 1
            elif key == 'q_3' and isinstance(value, (int, float)):
                system_message += f"Their workload manageability is rated {value}/5. "
                stress_level = 6 - value  # Invert scale for stress level (5 = low stress, 1 = high stress)
                count += 1
        
        # Process text responses
        for key, value in survey_responses.items():
            if key == 'q_9' and value and isinstance(value, str):
                system_message += f"They described their feelings about work: '{value}'. "
            elif key == 'q_10' and value and isinstance(value, str):
                system_message += f"They suggested workplace improvements: '{value}'. "
        
        # Add guidance based on scores
        if count > 0:
            avg_score = (wellbeing_score + work_life_balance + (6-stress_level))/3 if count == 3 else None
            
            if avg_score is not None:
                if avg_score < 2.5:
                    system_message += "The user appears to be struggling significantly. Provide empathetic support, validate their feelings, and suggest specific wellbeing strategies. "
                elif avg_score < 3.5:
                    system_message += "The user appears to be facing moderate challenges. Offer balanced advice focusing on small improvements and self-care. "
                else:
                    system_message += "The user appears to be doing relatively well. Focus on maintaining wellbeing and preventative strategies. "
    
    system_message += """
    Guidelines for responses:
    1. Be empathetic, warm, and supportive.
    2. Keep responses concise (2-3 sentences) and conversational.
    3. Provide practical, actionable advice when appropriate.
    4. Ask follow-up questions to better understand their situation.
    5. Do not diagnose medical conditions or provide clinical advice.
    6. Respect privacy and confidentiality.
    7. Use a supportive, friendly tone throughout.
    
    Topics to focus on:
    - Stress management and resilience
    - Work-life balance strategies
    - Team dynamics and psychological safety
    - Communication techniques
    - Self-care and wellbeing practices
    """
    
    # Construct the messages array for the OpenAI API
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    # Add chat history
    for message in chat_history:
        if message["role"] in ["user", "assistant"]:
            messages.append({"role": message["role"], "content": message["content"]})
    
    # Add the user's current message
    messages.append({"role": "user", "content": user_input})
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble connecting right now. Please try again later. Error: {str(e)}"

def get_initial_message(survey_responses=None):
    """
    Generates an initial message from the AI assistant based on survey responses.
    
    Args:
        survey_responses (dict): Dictionary containing the user's survey responses
    
    Returns:
        str: The AI's initial message
    """
    
    system_message = "You are an empathetic wellbeing assistant for a workplace mental health platform. "
    
    if survey_responses:
        system_message += "The user has just completed a wellbeing survey. "
        
        # Extract scores to determine overall tone
        wellbeing_score = survey_responses.get('q_1', 0)
        work_life_balance = survey_responses.get('q_2', 0)
        workload = survey_responses.get('q_3', 0)
        
        # Calculate average score if we have valid values
        valid_scores = [s for s in [wellbeing_score, work_life_balance, workload] if isinstance(s, (int, float)) and s > 0]
        avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None
        
        if avg_score is not None:
            if avg_score < 2.5:
                system_message += "Their responses indicate they're struggling with workplace wellbeing. "
            elif avg_score < 3.5:
                system_message += "Their responses indicate moderate workplace wellbeing challenges. "
            else:
                system_message += "Their responses indicate they're doing relatively well with workplace wellbeing. "
    
    system_message += """
    Generate a brief initial greeting message from 'Hurdl' (the assistant) to start a conversation about workplace wellbeing.
    The message should:
    1. Thank them for completing the survey
    2. Introduce yourself as Hurdl, a wellbeing assistant
    3. Ask an open-ended question to start the conversation about how they're feeling at work
    4. Keep it short, 2-3 sentences maximum
    5. Be warm, friendly and empathetic
    """
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "I've just completed the wellbeing survey. What now?"}
    ]
    
    # Convert to proper message types for the API
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return "Thanks for completing the survey! I'm Hurdl, your wellbeing assistant. How are you feeling about work this week?"