# UniMind: UoBrain – A Smart Mental Health Companion for Students

**UoBrain** is a student-focused mental health prototype designed to help track moods, analyze patterns, and offer personalized suggestions. It lets students log how they feel daily, write journal entries if they want to, and uses simple predictive tools to highlight any signs of distress. It also shares helpful resources—or emergency contacts when needed.

It’s built with Flask (as permitted via Marcel Skudlarski), following a modular MVC pattern, and includes features like mood simulation, VADER sentiment analysis from NLTK (Natural Language Toolkit), and basic machine learning. It’s not meant to replace professional help—but acts as a support tool to help students better understand their mental well-being.

---

## Project Structure (MVC Layout)

```
BUSPart2-main/
├── .flaskenv                # Flask environment variables loader
├── config.py                # App settings and configuration
├── requirements.txt         # Package dependencies
├── run.py                   # App launcher
├── README.md                # README file
├── app/                     
│   ├── __init__.py          # Flask app and SQLAlchemy setup
│   ├── models.py            # Models – (User, Mood_DB, EmergencyContact)
│   ├── views.py             # View – Flask routes & request handlers
│   ├── controller.py        # Controller – Core logic
│   ├── adapter.py           # External API adapter (simulated)
│   ├── domain.py            # Domain Model – MoodEntry logic & sentiment analysis
│   ├── forms.py             # View – Forms for mood/journal inputs
│   └── templates/           
│       ├── base.html        #   Base layout
│       ├── home.html        #   Home page
│       ├── log_mood.html    #   Mood Selection UI
│       ├── journal.html     #   Journal Entry UI
│       ├── predict.html     #   Prediction Results UI
│       ├── data.html        #   Historical Entries UI
│       └── errors/          #   Error page templates
│           ├── 403.html
│           ├── 404.html
│           ├── 413.html
│           └── 500.html
├── tests/                   
│   ├── test_distress_alert.py  # Tests for DistressAlert logic (Controller/Model)
│   └── test_recommendations.py # Tests for recommendation logic (Controller)

```

---

## Getting Started

### 1. Clone this repo:
```bash
git clone https://github.com/treboRS3003/BUSPart2.git
cd BUSPart2
```

### 2. Set up a virtual environment:
```bash
python3 -m venv venv
# macOS / Linux:
source venv/bin/activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 3. Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set environment variables:
Create a `.flaskenv` file:
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

### 5. Launch the app:
```bash
flask run
```
Open `http://127.0.0.1:5000` in your browser.

### 6. To run tests:
```bash
pip install pytest
pytest
```
---

## Requirements (Packages and Versions)

```
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
greenlet==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
SQLAlchemy==2.0.39
typing_extensions==4.12.2
Werkzeug==3.1.3
nltk==3.8.1
```

Make sure to download the VADER lexicon:
```python
import nltk
nltk.download('vader_lexicon')
```

---

## Technologies Involved
- **Python 3.10+**
- **Flask** (web framework)
- **Flask-SQLAlchemy** (ORM)
- **Flask-WTF** (form validation)
- **NLTK** (VADER for sentiment analysis)
- **HTML/CSS** with Jinja2 templating

---

## Key Features (Core Funtionalities Implemented)
As stated in an email with Wendy, our group was only required to implement 2 features as we are without a group member. However, we had already implemented three features upon recieving this email. The following features from assignment 1 are implemented:

### 1. **User Input**

  **Daily Mood Logging**
  Students choose from 12 mood buttons. Entries are saved with timestamps for tracking.
  - Code reference: `views.py` - app.route('log_mood'), `forms.py`- ChooseForm, `controller.py` - process_log_mood, `models.py` - Mood_DB
  - Positive: Mood logs correctly
  - Negative: No selection = warning prompt

  **Journal Sentiment Analysis**
  After logging mood, students can write journal entries. These are scored using VADER.
  - Code reference: `views.py` - app.route('journal'), `forms.py` - JournalForm, `controller.py` - process_journal, `models.py` - Mood_DB.sentiment_score,`domain.py` - MoodEntry_performAnalysis
  - Uses dependency between MoodEntry and SentimentAnalysis
  - Positive: Stores sentiment score into Mood_DB row
  - Negative: Skips analysis, stores Null value.

### 2. **Data Integration**
A mock external API combines weather + wearable data with schedule info to simulate predictions. Furthermore, data about the user's schedule is input.
- Code reference: `adapter.py` - ExternalAPIAdapter.fetch_mood_entry, `domain.py` - MoodEntry, `controller.py` - process_prediction, `models.py` - Mood_DB.weather, Mood_DB.smartwatch_data, Mood_DB.timetable
- Uses Adapter Pattern via `ExternalAPIAdapter`
- Updates the database with fetched data. (Note that entries into the database are dependent on the date)
- If data is unavailable, only the fetched data is stored.  

### 3. **Emergency Support / Suggestions**
In response to predicted mood and in the case of evident distress (7 consecutive negative mood entries), support/advice and resources are prompted.
- Code reference: `views.py` - journal/predict, `controller.py` - class DistressAlert, class SupportService, class RecommendationSystem,process_recommendation, `models.py` - EmergencyContact
- Positive: Congratulatory message and relevant links
- Negative: Support message and relevant links
- Distress: In situation of 7 consecutive negative mood entries input , redirect to distress page. Page provides User's Emergency Contact and recommendations.

**This concludes the three main features implemented for our prototype.**

### 4. **Mood Prediction (Simulated)**
Due to the complexity of the machine learning model, it has not been implemented in this prototype. However, the prediction is crucial for the prototype and as such has been simulated through hardcoded values.
- Code reference: `views.py` - predict, `controller.py` - class PredictionModel,process_prediction

### 5. **Simulate Buttons**
In accordance with assignment 1, two buttons have been introduced to our prototype. Both are found in `views.py`
- Simulate 6pm redirects the user to log their mood.
- Simulate 8am redirects to mood prediction.
---

## Pytests

### 1. **test_recommendations.py**
Ensures mood is correctly identified as positive/negative or invalid. Subsequently, further tests ensure the correct output of messages and suggestions are given.
More detail is given in the code.

### 2. **test_distress_alert.py**
Unit tests to ensure Distress_Alert is activated if and only if there exist 7 consecutive negative mood entries. Note that testing the retrieval of 7 previous data entries should be implemented during integration testing. More detail is given in the code.

## Design Patterns & Class Structure

- **Design Pattern Used**: Adapter Pattern (`ExternalAPIAdapter` wraps third-party data as `MoodEntry`)
- **Class Relationships**:
  - **Association**: `User` associated with `EmergencyContact` (One-to-one).
  - **Inheritance**: `User` inherits `UserMixin` for authentication.
  - **Dependency**: `MoodEntry` depends on `SentimentAnalysis`

---

## Team Contributions

| Student Name & ID        | Contribution (%) | Key Contributions / Tasks Completed                              | Comments (if any) | Signature |
| ------------------------ | ---------------- | ----------------------------------------------------------------- | ----------------- | --------- |
| Chiamaka Agu (2333717) |                  |                                                                 |                   |           |
| Samuel Cardew (2829319 )|                  |                                                                 |                   |           |
| Charles Egornu (2767047)|                  | Wrote this README and ensured it meets assignment specs           |                   |           |
| Robert Saunders (2269091)|                  | Wrote all code in Initial Commit and edited README   |                   |           |

---

## Notes to Keep in Mind

- Mood prediction is simulated—it’s not advanced machine learning.
- Sentiment scoring is basic (just VADER).
- A distress alert is sent after 7 negative moods in a row.
- There’s no current user login just a preset user that loads on launch.
- This app is a **support tool**, not a substitute for mental health care.

---

Everything here is based on what’s actually built into the UoBrain prototype. For a deeper dive into the technical stuff, check out the code.
