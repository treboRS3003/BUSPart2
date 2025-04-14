from unittest.mock import patch

import pytest

import app.controller
from app.controller import is_positive_mood, create_message

"""
test_process_recommendation_positive tests the process_recommendation function to check that the congratulatory message
is received when the predicted mood is positive.
"""
def test_process_recommendation_positive():
    pass


"""
test_process_recommendation_negative tests the process_recommendation function to check that the user does not receive a 
congratulatory message or support message when the predicted mood is not in the MOOD_LIST []. 
"""
def test_process_recommendation_negative():
    pass


"""
test_is_positive_mood_positive tests the is_positive_mood function to check that it returns True when a positive
mood contained in the positive_moods list is input as the predicted_mood parameter. 
"""
@pytest.mark.parametrize("predicted_mood", ['Happy', 'Optimistic', 'Calm', 'Content', 'Excited', 'Energetic'])
def test_is_positive_mood_positive(predicted_mood):
    assert is_positive_mood(predicted_mood) is True


"""
test_is_positive_mood_negative tests the is_positive_mood function to check that it returns False when a negative 
mood not contained in the positive_moods list is input as the predicted_mood parameter. 
"""
@pytest.mark.parametrize("predicted_mood", ['Sad', 'Angry', 'Anxious', 'Neutral', 'Tired', 'Stressed'])
def test_is_positive_mood_negative(predicted_mood):
    assert is_positive_mood(predicted_mood) is False


"""
test_create_message_positive tests the is_positive_mood function to check that it returns the intended message when a 
negative mood is input as the predicted_mood parameter. 
"""
def test_create_message_positive():
    with patch('app.controller.is_positive_mood') as mock_fetch:
        mock_fetch.return_value = False
        result = create_message("Sad")
        assert result == ("It seems you're experiencing a challenging mood. Consider these suggestions "
                          "and feel free to seek additional support.")


"""
test_create_message_negative tests the is_positive_mood function to check that it returns a XXXX Error when an unknown
mood not contained in the positive_moods or negative_moods list is input as the predicted_mood parameter. 
"""
def test_create_message_negative():
    pass

