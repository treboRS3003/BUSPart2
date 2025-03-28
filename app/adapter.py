
import random
from abc import ABC, abstractmethod
from datetime import datetime
from app.domain import MoodEntry

"""
Focuses on getting API data as shown in class diagram whilst conforming to an adapter pattern
"""

class MoodEntryAdapter(ABC):
    @abstractmethod
    def fetch_mood_entry(self) -> MoodEntry:
        """
        Convert the source-specific data into a unified MoodEntry.
        """
        pass

class WearableData:
    """
    Simulates a wearable device that tracks heart rate, steps, and sleep.
    Random values are generated for demonstration purposes.
    Ensured heart rate and step count are integers and sleep_quality is float as dictated in class diagram
    Removed dataID from class diagram
    Note in functional requirement we state to collect the physiological data every 5 minutes .
    This is unnecessary, we collect total step count, hours of sleep quality and average heart rate.
    """
    def __init__(self, user_id: int):
        self.user_id = user_id
        # Random heart rate between 60 and 100
        self.heart_rate = random.randint(60, 100)
        # Random step count between 0 and 20,000
        self.step_count = random.randint(0, 20000)
        # Random sleep quality between 4.0 and 10.0 (rounded to 1 decimal)
        self.sleep_quality = round(random.uniform(4.0, 10.0), 1)

    def get_heart_rate(self):
        return self.heart_rate

    def get_step_count(self):
        return self.step_count

    def get_sleep_quality(self):
        return self.sleep_quality

class ExternalAPI:
    """
    Simulates an external API that can provide both weather data
    and wearable-like data for a user.
    """
    def __init__(self, api_id: int, api_name: str, api_key: str):
        self.api_id = api_id
        self.api_name = api_name
        self.api_key = api_key
        self.weather_options = ["Sunny", "Rainy", "Cloudy", "Stormy", "Snowy", "Windy"]

    def fetch_weather_data(self):
        # Randomly pick one of the 6 weather options
        return random.choice(self.weather_options)

    # Uses dependency on WearableData as stated in class diagram
    def fetch_wearable_data(self, user_id: int):
        wearable_instance = WearableData(user_id)
        # Return a dict that simulates wearable data
        heart_rate = wearable_instance.get_heart_rate()
        step_count = wearable_instance.get_step_count()
        sleep_quality = wearable_instance.get_sleep_quality()

        return {
            "user_id": user_id,
            "heart_rate": heart_rate,
            "step_count": step_count,
            "sleep_quality": sleep_quality
        }



class ExternalAPIAdapter(MoodEntryAdapter):
    def __init__(self, external_api: ExternalAPI, user_id: int):
        self.external_api = external_api
        self.user_id = user_id

    def fetch_mood_entry(self) -> MoodEntry:
        weather = self.external_api.fetch_weather_data()
        wearable_data = self.external_api.fetch_wearable_data(self.user_id)
        # Use the external API data to build a MoodEntry.
        mood_text = "Neutral"  # Again, determine mood based on your logic.
        mood_entry = MoodEntry(
            user_id=wearable_data["user_id"],
            date=datetime.now().date(),
            smartwatch_data=f"HR: {wearable_data['heart_rate']}, Steps: {wearable_data['step_count']},SQ: {wearable_data['sleep_quality']}",
            weather=weather,

        )
        return mood_entry