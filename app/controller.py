from flask import flash
from app import db
from app.models import Mood_DB
from datetime import datetime
from app.adapter import ExternalAPI, ExternalAPIAdapter
import random
from app.domain import MoodEntry



MOOD_LIST = [
    "Happy", "Sad", "Angry", "Excited", "Calm", "Anxious",
    "Content", "Stressed", "Bored", "Energetic", "Melancholic", "Optimistic"
]

"""domain classes"""


"""
Identical to class diagram
"""
class UserMonthlyReport:
    def __init__(self):
        self.reportID = random.randint(1, 10000)
        self.userID = random.randint(1, 9999)
        self.exerciseHours = random.randint(0, 30)
        self.lectureHours = random.randint(0, 50)
        self.workHours = random.randint(0, 160)
        self.deadlines = random.randint(0, 10)

    def submitReport(self) -> dict:
        return {
            "reportID": self.reportID,
            "userID": self.userID,
            "exerciseHours": self.exerciseHours,
            "lectureHours": self.lectureHours,
            "workHours": self.workHours,
            "deadlines": self.deadlines
        }

"""
Added is_trained in order to avoid retraining the model each time.
Prototype is not too concerned about the functionality of the model, for example we do not use synthetic data 
for a month and retrain each month and we randomise the predicted emotion.
Otherwise the class functionality remains the same and entries.
"""
class PredictionModel:
    def __init__(self):
        self.is_trained = False
        self.data = None

    def train(self):
        self.data = Mood_DB.query.all()
        self.is_trained = True
        print("PredictionModel: Training completed on provided data.")
        print(f"PredictionModel: Training on {len(self.data)} entries.")

    def predict(self) -> str:
        if not self.is_trained:
            flash("Model not trained", "warning")
            return "Neutral"
        possible_predictions = MOOD_LIST
        return random.choice(possible_predictions)

    def regression_imputation(self):
        return


"""
Ensures FR6 is achieved 
"""
class SupportService:
    """
    Provides information about available support services.
    Matches the class diagram attributes/methods:
      supportID: int
      serviceName: String
      getSupportService()
      externalWellBeing()
      removed  the contactsinfo parameter
    """
    def __init__(self, supportID: int, serviceName: str, user_id: int):
        self.supportID = supportID
        self.serviceName = serviceName
        self.user_id = user_id

    def getSupportContacts(self) -> str:
        """
        Returns a brief description of the support service including the user's emergency contact.
        """
        from app.models import User
        user = User.query.get(self.user_id)
        if not user or not user.emergency_contact:
            return "No emergency contact info available."
        ec = user.emergency_contact
        return f"Consider contacting your emergency contact: {ec.full_name}, {ec.contact_number}"

    def externalUniWellBeing(self):
        """
        Returns additional external resources or contact info.
        assume for prototype that the student is from university of birmingham
        """
        message = "Please consider contacting your University Wellbeing team at 0800 368 5819"
        return message


"""
Class remains the same except suggestions is not a list it is a dictionary.
for the purpose of the prototype links and descriptions have been gathered using chat gpt.
"""
class RecommendationSystem:
    def __init__(self, user_id):
        self.user_id = user_id
        # A dictionary that maps each mood to a structured recommendation.
        # "links" might point to yoga, breathing exercises, etc.
        self.suggestions = {
            "Happy": {
                "description": "You’re in a good mood! Keep up the positive energy.",
                "tips": [
                    "Keep a gratitude journal to reflect on positive events.",
                    "Share your joy with someone—send a message to a friend."
                ],
                "links": [
                    {"name": "Yoga Journal", "url": "https://www.yogajournal.com/"},
                    {"name": "Headspace Mindfulness", "url": "https://www.headspace.com/mindfulness"}
                ]
            },
            "Sad": {
                "description": "It’s normal to feel down sometimes. Here are ways to cope:",
                "tips": [
                    "Try a gentle yoga flow to lift your spirits.",
                    "Reach out to a trusted friend or counselor."
                ],
                "links": [
                    {"name": "Yoga Blues", "url": "https://www.yogajournal.com/poses/yoga-for-depression/"},
                    {"name": "Breathing exercises",
                     "url": "https://www.healthline.com/health/breathing-exercise-for-anxiety"}
                ]
            },
            "Angry": {
                "description": "Anger can be overwhelming, but you can manage it healthily.",
                "tips": [
                    "Practice a breathing exercise for 5 minutes to calm down.",
                    "Channel your energy into something constructive, like a workout."
                ],
                "links": [
                    {"name": "Box Breathing Technique", "url": "https://www.healthline.com/health/box-breathing"},
                    {"name": "Managing Anger Tips",
                     "url": "https://www.verywellmind.com/tips-for-managing-anger-4158310"}
                ]
            },
            "Excited": {
                "description": "You’re bursting with energy! Make the most of it.",
                "tips": [
                    "Plan or start a fun project you’ve been putting off.",
                    "Write down your goals to harness this excitement productively."
                ],
                "links": [
                    {"name": "Goal Setting Tools", "url": "https://www.mindtools.com/a4wo118/goal-setting"},
                    {"name": "Motivational Video", "url": "https://www.youtube.com/watch?v=9kzQ9ZgZCRg"}
                ]
            },
            "Calm": {
                "description": "Enjoy your calm state. Here are some ideas to maintain it:",
                "tips": [
                    "Try a short meditation session to reinforce your peace.",
                    "Listen to relaxing music or a guided mindfulness session."
                ],
                "links": [
                    {"name": "Calm App", "url": "https://www.calm.com/"},
                    {"name": "Headspace", "url": "https://www.headspace.com/"}
                ]
            },
            "Anxious": {
                "description": "Anxiety can be tough. Consider these ways to find relief:",
                "tips": [
                    "Try mindful breathing exercises for 5–10 minutes.",
                    "Talk to someone supportive or write down your worries."
                ],
                "links": [
                    {"name": "Breathing Exercise",
                     "url": "https://www.healthline.com/health/breathing-exercise-for-anxiety"},
                    {"name": "Anxiety UK", "url": "https://www.anxietyuk.org.uk/"}
                ]
            },
            "Content": {
                "description": "You’re feeling content. Keep doing what works!",
                "tips": [
                    "Enjoy a quiet moment to reflect on your achievements.",
                    "Share your sense of well-being with someone who matters to you."
                ],
                "links": [
                    {"name": "Contentment Info", "url": "https://www.verywellmind.com/what-is-contentment-4771990"},
                    {"name": "Gratitude Apps", "url": "https://positivepsychology.com/gratitude-apps/"}
                ]
            },
            "Stressed": {
                "description": "Feeling stressed? Try these techniques to unwind:",
                "tips": [
                    "Practice a short yoga session to relax tense muscles.",
                    "Take a 10-minute break and do a quick breathing exercise."
                ],
                "links": [
                    {"name": "Yoga for Stress", "url": "https://www.yogajournal.com/poses/yoga-for-stress/"},
                    {"name": "Breathing Meditation", "url": "https://www.mindful.org/breathing-meditation-2/"}
                ]
            },
            "Bored": {
                "description": "Boredom can be an opportunity to explore new things:",
                "tips": [
                    "Pick up a new hobby, or revisit an old interest.",
                    "Try a quick workout or a new recipe to spark excitement."
                ],
                "links": [
                    {"name": "Productive Ideas",
                     "url": "https://www.lifehack.org/articles/lifestyle/15-productive-things-bored.html"},
                    {"name": "Yoga with Adriene", "url": "https://www.youtube.com/user/yogawithadriene"}
                ]
            },
            "Energetic": {
                "description": "You have lots of energy! Channel it wisely:",
                "tips": [
                    "Go for a run or do a high-intensity workout.",
                    "Use this energy to tackle challenging tasks on your to-do list."
                ],
                "links": [
                    {"name": "Runner's World UK", "url": "https://www.runnersworld.com/uk/"},
                    {"name": "High-Intensity Workout", "url": "https://www.youtube.com/watch?v=ml6cT4AZdqI"}
                ]
            },
            "Melancholic": {
                "description": "You’re feeling melancholic. Here are gentle suggestions:",
                "tips": [
                    "Listen to soothing music or try journaling your thoughts.",
                    "Give yourself space to process emotions, and seek help if needed."
                ],
                "links": [
                    {"name": "Managing Sadness", "url": "https://www.verywellmind.com/ways-to-manage-sadness-3144938"},
                    {"name": "BetterHelp", "url": "https://www.betterhelp.com/"}
                ]
            },
            "Optimistic": {
                "description": "You’re feeling optimistic! Keep the positive outlook going.",
                "tips": [
                    "Share your optimism with friends or family.",
                    "Plan a fun activity that aligns with your goals."
                ],
                "links": [
                    {"name": "Learned Optimism", "url": "https://positivepsychology.com/learned-optimism/"},
                    {"name": "Optimistic Inspiration", "url": "https://www.youtube.com/watch?v=Uxl3IGXa3MY"}
                ]
            }
        }

    def generate_recommendations(self, mood: str) -> dict:
        """
        Returns a dictionary with 'description', 'tips', and 'links'
        for the given mood. If the mood is not found, returns a default fallback.
        """
        return self.suggestions.get(mood, {
            "description": "No specific recommendations found for this mood.",
            "tips": [],
            "links": []
        })


"""
Distress alert class
"""
class DistressAlert:
    def __init__(self, user_id: int, message: str = "Distress Alert Triggered"):
        self.user_id = user_id
        self._message = message

    #Checks if last 7 entries are negative entries and if so return True
    def triggerAlert(self, current_mood_record) -> bool:
        previous_entries = (
            Mood_DB.query.filter(
                Mood_DB.user_id == self.user_id,
                Mood_DB.date < current_mood_record.date
            )
            .order_by(Mood_DB.date.desc())
            .limit(7)
            .all()
        )
        #CHecks there are 7 previous entries
        if len(previous_entries) == 7:
            #returns true if there are 7 previous sentiment scores all below 0 or mood entered for the past 7 entries are negative
            distress_triggered = all(
                (entry.sentiment_score is not None and entry.sentiment_score < 0) or
                (entry.mood.lower() in [ "Sad", "Angry", "Anxious", "Stressed", "Bored", "Melancholic"])
                for entry in previous_entries
            )
            return distress_triggered
        return False

    #Gets information about emergency support
    def contactEmergencySupport(self):
        from app.models import User
        user = User.query.get(self.user_id)
        if not user:
            flash(f"[DistressAlert] No user found with ID {self.user_id}.", "warning")
            return
        ec = user.emergency_contact
        if not ec:
            flash(f"[DistressAlert] No emergency contact found for user {user.full_name}.", "warning")
            return
        flash(
            f"[DistressAlert] Contacting {ec.full_name} at {ec.contact_number} for user {user.full_name}. "
            f"Message: {self._message}",
            "warning"
        )


"""controller functions"""


def process_recommendation(user, predicted_mood):
    """
    Processes recommendations based on the predicted mood.
    Aligns with FR6:
      - Congratulatory message if mood is positive (Happy, Optimistic, etc.).
      - Support suggestions and external help if mood is negative.

    Also integrates the SupportService class from the class diagram
    to provide external well-being info or help links.
    """
    # Instantiate the RecommendationSystem with the current user's ID.
    recommendation_system = RecommendationSystem(user_id=user.id)

    # Retrieve suggestions from the recommendation system based on the predicted mood.
    suggestions = recommendation_system.generate_recommendations(predicted_mood)

    # Decide which moods are "positive" vs. "negative"
    positive_moods = ["Happy", "Optimistic", "Calm", "Content", "Excited", "Energetic"]

    # If the predicted mood is positive, display a congratulatory message
    if predicted_mood in positive_moods:
        message = (
            "Congratulations! Your mood is positive. Keep up the great work! "
            "Here are some tips to stay on this track:"
        )
        # For a positive mood, we typically don't need external support info
        support_contact = None
        uni_wellbeing = None
    else:
        # Negative or neutral moods get a support message
        message = (
            "It seems you're experiencing a challenging mood. Consider these suggestions "
            "and feel free to seek additional support."
        )
        # Instantiate the SupportService (example values for ID, name, noticeDouble)
        support_service = SupportService(
            supportID=101,
            serviceName="UniMind Student Support",
            user_id=user.id

        )
        support_contact = support_service.getSupportContacts()
        uni_wellbeing = support_service.externalUniWellBeing()

    # Return a dictionary containing the main message, the suggestions, and any support info
    return {
        "message": message,
        "suggestions": suggestions,
        "support_contact": support_contact,
        "Uni_wellbeing": uni_wellbeing

    }

def process_log_mood(choice, user):
    """Processes mood selection and returns the Mood_DB record."""
    from app.models import Mood_DB
    today = datetime.now().date()
    #collects first entry of data in database that of the current day
    mood_record = Mood_DB.query.filter_by(user_id=user.id, date=today).first()
    #if today's mood record exists simply just add the mood to the database
    if mood_record:
        mood_record.mood = choice
        # we commit this to the database here as instruction in the first sequence diagram in assignment 1
        db.session.commit()

    #otherwise create a new mood record for today with the selected mood
    else:
        mood_record = Mood_DB(
            user_id=user.id,
            date=today,
            mood=choice
        )
        #We create a domain-level MoodEntry object to encapsulate the mood data and handle additional data
        mood_entry = MoodEntry(user_id=user.id, date=today, mood=choice)
        #add it to the database like done in sequence diagram
        mood_entry.storeEntry()
        # Reload the record from the DB
        mood_record = Mood_DB.query.filter_by(user_id=user.id, date=today).first()
    return mood_record

def process_journal(mood_id, journal_text, user):
    """Processes journal text by analyzing sentiment and updating the record."""
    from app.models import Mood_DB
    #retrieve the entry via the mood_id this is just the daily entry as this object will be created by now
    db_record = Mood_DB.query.get(mood_id)

    #failsafe if mood isn't input (not really needed)
    if not db_record:
        return None, "No mood record found."

    #create a MoodEntry domain object to encapsulate the mood data and any logic around it.
    # This is done as it is easier to implement and update. When scaling up this becomes more important
    mood_entry = MoodEntry(
        user_id=db_record.user_id,
        date=db_record.date,
        mood=db_record.mood
    )

    #add the existing sentiment score to the domain object (currently it will be none)
    mood_entry.sentiment_score = db_record.sentiment_score

    #checks if the user provided some text
    if journal_text:
        #calls the domain object function to analyse the text
        mood_entry.analyzeSentiment(journal_text)
        #stores this entry into the database
        mood_entry.storeEntry()

    #returns the mood entry object and None as a success message
    return mood_entry, None

def process_prediction(user):
    """Processes the prediction flow and returns the predicted mood."""
    from app.models import Mood_DB
    #Get today's date
    today = datetime.now().date()
    #find the record of today's date in the database
    mood_record = Mood_DB.query.filter_by(user_id=user.id, date=today).first()

    #create an external api object
    external_api = ExternalAPI(api_id=2, api_name="OpenWeather", api_key="ABC123")
    adapter = ExternalAPIAdapter(external_api, user_id=user.id)
    #fetch the data
    external_data = adapter.fetch_mood_entry()
    extra_smartwatch = external_data.smartwatch_data

    # Generate timetable information using a monthly report.
    monthly_report = UserMonthlyReport()
    #retrieve monthly report data (e.g., hours of exercise, lectures, work, deadlines).
    report_data = monthly_report.submitReport()
    timetable = (
        f"Exercise H: {report_data['exerciseHours']}, Lecture H: {report_data['lectureHours']},"
        f"Work H: {report_data['workHours']}, Num Deadlines: {report_data['deadlines']}"
    )
    # If there's no mood record for today, create one and populate fields with external data and timetable.
    if not mood_record:
        mood_record = Mood_DB(
            user_id=user.id,
            date=today,
            smartwatch_data=extra_smartwatch,
            weather=external_data.weather,
            timetable=timetable
        )
        db.session.add(mood_record)
    else:
        #update record with the data
        mood_record.weather = external_data.weather
        mood_record.smartwatch_data = extra_smartwatch
        mood_record.timetable = timetable
    #commit all changes to the database
    db.session.commit()

    # Train and predict using the model.
    model = PredictionModel()
    model.train()
    predicted_mood = model.predict()
    return predicted_mood