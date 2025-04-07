from datetime import datetime, timedelta
from app.controller import DistressAlert


"""
class FakeMoodEntry is used instead of the Mood_DB model to allow us to input test values to carry out our unit tests on, 
rather than having to use actual data from the Mood_DB database. 

create_test_mood_entries is a function used to create fake mood entries for the purpose of testing our DistressAlert 
feature without having to rely on real data from our Mood_DB database. 
"""
class FakeMoodEntry:
    def __init__(self, date, mood, sentiment_score):
        self.date = date
        self.mood = mood
        self.sentiment_score = sentiment_score

def create_test_mood_entries(number_of_days, negative=True):
    test_entries = []
    for i in range(number_of_days):
        mood_date = datetime.now() - timedelta(days=i+1)
        if negative:
            test_entries.append(FakeMoodEntry(mood_date, "Sad", -0.7))
        else:
            test_entries.append(FakeMoodEntry(mood_date, "Happy", 0.7))
    return test_entries


"""
test_triggerAlert_positive tests the triggerAlert function to check that True is returned if the user has 7 consecutive
negative mood entries.
"""
def test_triggerAlert_positive():
    pass


"""
test_triggerAlert_positive tests the triggerAlert function to check that 
"""
def test_triggerAlert_negative():
    pass


"""
test_check_for_negative_entries_positive tests the check_for_negative_entries function to ensure True is returned if the 7 
previous consecutive mood entries have been negative. 
"""
def test_check_for_negative_entries_positive():
    test_entries = create_test_mood_entries(7, negative=True)

    assert DistressAlert(user_id=1).check_for_negative_entries(test_entries) is True


"""
test_check_for_negative_entries_negative tests the check_for_negative_entries function to ensure False is returned if there are 
only 6 previous consecutive mood entries. 
"""
def test_check_for_negative_entries_negative():
    test_entries = create_test_mood_entries(6, negative=True)

    assert DistressAlert(user_id=1).check_for_negative_entries(test_entries) is False

