"""
introduced this file to ensure no circular import between app.controller and app.adapter
"""
from datetime import datetime
from app import db
from app.models import Mood_DB

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class MoodEntry:
    """
    A domain-level class representing a mood entry with functionality to store data
    in the database and perform sentiment analysis.
    Restructured from class diagram in terms of inputs, however the functions remain the same.
    """
    def __init__(self, user_id: int = 1, date=None, mood: str = "NA",
                 smartwatch_data: str = None, weather: str = None, timetable: str = None):
        self.user_id = user_id
        self.date = date or datetime.now().date()
        self.mood = mood
        self.smartwatch_data = smartwatch_data
        self.weather = weather
        self.timetable = timetable
        self.sentiment_score = None  # To be set after analysis

    def storeEntry(self) -> Mood_DB:
        record = Mood_DB.query.filter_by(user_id=self.user_id, date=self.date).first()
        if record:
            if self.mood is not None:
                record.mood = self.mood
            if self.sentiment_score is not None:
                record.sentiment_score = self.sentiment_score
            if self.smartwatch_data is not None:
                record.smartwatch_data = self.smartwatch_data
            if self.weather is not None:
                record.weather = self.weather
            if self.timetable is not None:
                record.timetable = self.timetable
        else:
            record = Mood_DB(
                user_id=self.user_id,
                date=self.date,
                mood=self.mood,
                sentiment_score=self.sentiment_score,
                smartwatch_data=self.smartwatch_data,
                weather=self.weather,
                timetable=self.timetable
            )
            db.session.add(record)
        db.session.commit()
        return record


    """
    This is a great example of a relationship that has been coded and was shown in the class diagram.
     MoodEntry having a dependency on Sentiment Analysis for this function to work.
    """
    def analyzeSentiment(self, text: str):
        analysis = SentimentAnalysis(moodEntryID=0, text=text)
        analysis.performAnalysis()
        self.sentiment_score = analysis.getScore()
        existing_record = Mood_DB.query.filter_by(user_id=self.user_id, date=self.date).first()
        if existing_record:
            existing_record.sentiment_score = self.sentiment_score
            db.session.commit()


"""
Added text from class diagram
otherwise same as class diagram
"""
class SentimentAnalysis:
    def __init__(self, moodEntryID: int, text: str = ""):
        self.analysisID = None
        self.moodEntryID = moodEntryID
        self._sentimentScore = None
        self.text = text

    def performAnalysis(self):
        if not self.text:
            self._sentimentScore = None
        else:
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(self.text)
            self._sentimentScore = scores['compound']

    def getScore(self) -> float:
        return self._sentimentScore
