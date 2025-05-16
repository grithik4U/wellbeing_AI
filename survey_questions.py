def get_survey_questions():
    """
    Returns the survey questions for the weekly check-in.
    
    Each question has:
    - id: unique identifier for the question
    - text: the question text
    - type: type of question (scale, text, radio, header)
    - options: for radio questions, a list of possible options
    """
    return [
        {
            "id": "wellbeing_header",
            "text": "Personal Wellbeing",
            "type": "header"
        },
        {
            "id": 1,
            "text": "Overall, how would you rate your wellbeing at work this week?",
            "type": "scale"
        },
        {
            "id": 2,
            "text": "I felt a good work-life balance this week.",
            "type": "scale"
        },
        {
            "id": 3,
            "text": "My workload felt manageable this week.",
            "type": "scale"
        },
        {
            "id": 4,
            "text": "I felt satisfied with my work this week.",
            "type": "scale"
        },
        {
            "id": "safety_header",
            "text": "Psychological Safety & Team Environment",
            "type": "header"
        },
        {
            "id": 5,
            "text": "I felt psychologically safe in my team this week.",
            "type": "scale"
        },
        {
            "id": 6,
            "text": "I felt comfortable speaking up and sharing ideas this week.",
            "type": "scale"
        },
        {
            "id": 7,
            "text": "I felt supported by my manager/team when I needed help.",
            "type": "scale"
        },
        {
            "id": 8,
            "text": "Mistakes are treated as opportunities to learn in my team.",
            "type": "scale"
        },
        {
            "id": "feedback_header",
            "text": "Open Feedback",
            "type": "header"
        },
        {
            "id": 9,
            "text": "How are you feeling about work this week? Any specific highs or lows?",
            "type": "text"
        },
        {
            "id": 10,
            "text": "Do you have any suggestions for improving our workplace or team environment?",
            "type": "text"
        }
    ]
