<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# WELLBEING_AI

<em>Empowering workplaces through wellbeing and insightful feedback.</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/grithik4U/wellbeing_AI?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/grithik4U/wellbeing_AI?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/grithik4U/wellbeing_AI?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
<img src="https://img.shields.io/badge/TOML-9C4121.svg?style=flat&logo=TOML&logoColor=white" alt="TOML">
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style=flat&logo=Plotly&logoColor=white" alt="Plotly">
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/uv-DE5FE9.svg?style=flat&logo=uv&logoColor=white" alt="uv">

</div>
<br>

---
https://github.com/user-attachments/assets/0fb7668f-750c-4f51-a03b-f08dba63f672
## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)

---

## Overview

wellbeing_AI is a comprehensive platform designed to enhance workplace mental health through data-driven insights and personalized support. 

**Why wellbeing_AI?**

This project aims to foster a healthier work environment by enabling organizations to gather, analyze, and act on employee feedback. The core features include:

- 🌟 **Database Management:** Efficiently stores and retrieves survey responses, ensuring data integrity.
- 📊 **Structured Survey Questions:** Facilitates meaningful insights into employee wellbeing and team dynamics.
- 📈 **Data Analysis Functions:** Provides actionable insights into employee sentiment and workload trends.
- 🎨 **Interactive Visualization:** Displays data through charts, enhancing understanding of workplace culture.
- 🤖 **AI Assistant Integration:** Offers personalized support and guidance for mental wellness.
- How the Survey, AI Analysis, and Chatbot Work
Survey Response Processing
The application collects survey responses with several technical layers:

- Data Collection: When a user completes the survey, we collect responses to 10 questions covering wellbeing, work-life balance, psychological safety, and open feedback.
Database Storage:
Responses are stored in a SQLite database with anonymized identifiers
The save_response function in database.py saves each response with a UUID
This creates a persistent record while maintaining user anonymity
Data Structuring:
Quantitative responses (1-5 scale questions) are stored as numeric values
Qualitative responses (text questions) are stored as strings
Metadata like department and location are stored alongside responses
- AI Analysis Systems
The platform uses several NLP and analytical techniques:

- Sentiment Analysis:
The analyze_sentiment function in data_analysis.py processes text responses
We use TextBlob's sentiment analysis (a Python NLP library) to assess polarity scores
Text is converted from a -1 to 1 scale to a 1-5 scale for consistency
This extracts emotional tone without requiring explicit emotion ratings
- Topic Analysis:
Text responses are tokenized (split into words)
Stop words are filtered out to focus on meaningful terms
Word frequencies are calculated to identify common themes
Predefined topic categories (workload, team, management, growth) are matched against response content
- Trend Detection:
The detect_trends function compares current data with previous periods
Statistical thresholds determine significant changes in wellbeing metrics
When metrics change beyond thresholds, alerts are generated with severity ratings
Both global and department-specific trends are monitored
AI Chatbot Implementation
- The chatbot uses sophisticated AI techniques:

- Context Building:
The generate_chatbot_response function in ai_assistant.py constructs a context from survey responses
Survey data is transformed into a system message that guides the AI assistant
The assistant's behavior adapts based on detected wellbeing scores (e.g., more supportive for lower scores)
- OpenAI Integration:
We use OpenAI's GPT-4o model through the OpenAI Python library
The newest model (gpt-4o) provides state-of-the-art conversational capabilities
The implementation uses the ChatCompletion API with temperature control for consistent responses
- Conversation Management:
Chat history is maintained in Streamlit's session state
Each message exchange is stored with role ("user" or "assistant") and content
Context window management ensures the conversation history fits within model limitations
- Response Generation:
The system creates a message structure with three components:
System prompt (containing survey context and behavioral guidelines)
Conversation history
Current user input
The AI generates responses tailored to the user's wellbeing state
Response formatting ensures concise, actionable advice (limited to 150 tokens)
The combination of these technologies creates an intelligent system that not only monitors workplace wellbeing but also provides personalized support through natural language interaction, demonstrating practical applications of NLP and conversational AI in the workplace mental health domain.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Uv

### Installation

Build wellbeing_AI from the source and intsall dependencies:

1. **Clone the repository:**





    ```sh
    ❯ git clone https://github.com/grithik4U/wellbeing_AI
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd wellbeing_AI
    ```

3. **Install the dependencies:**

**Using [uv](https://docs.astral.sh/uv/):**

```sh
❯ uv sync --all-extras --dev
```

### Usage

Run the project with:

**Using [uv](https://docs.astral.sh/uv/):**

```sh
uv run python {entrypoint}
```

### Testing

Wellbeing_ai uses the {__test_framework__} test framework. Run the test suite with:

**Using [uv](https://docs.astral.sh/uv/):**

```sh
uv run pytest tests/
```

---

<div align="left"><a href="#top">⬆ Return</a></div>

---
