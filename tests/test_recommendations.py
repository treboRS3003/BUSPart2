from unittest.mock import patch, MagicMock
import pytest
from app.controller import is_positive_mood, create_message, retrieve_support, process_recommendation

"""
test_process_recommendation_positive tests the process_recommendation function to check that the correct output is returned
when the predicted mood is negative. The classes and functions called by process_recommendation have been mocked. 
"""
def test_process_recommendation_positive():
    mock_user = MagicMock()
    mock_user.id = 111

    with patch('app.controller.RecommendationSystem') as mock_RecommendationSystem, \
            patch('app.controller.create_message') as mock_create_message, \
            patch('app.controller.is_positive_mood') as mock_is_positive_mood, \
            patch('app.controller.retrieve_support') as mock_retrieve_support:

        mock_recommendation_system = mock_RecommendationSystem.return_value
        mock_recommendation_system.generate_recommendations.return_value = "Example Suggestions"

        mock_is_positive_mood.return_value = False
        mock_create_message.return_value = (
            "It seems you're experiencing a challenging mood. Consider these suggestions "
            "and feel free to seek additional support."
        )
        mock_retrieve_support.return_value = ("Consider contacting your emergency contact: John Doe, 123456789", "Please consider contacting your University Wellbeing team at 0800 368 5819")

        result = process_recommendation(mock_user, "Sad")

        assert result['message'] == (
            "It seems you're experiencing a challenging mood. Consider these suggestions "
            "and feel free to seek additional support."
        )
        assert result['suggestions'] == "Example Suggestions"
        assert result['support_contact'] == "Consider contacting your emergency contact: John Doe, 123456789"
        assert result['Uni_wellbeing'] == "Please consider contacting your University Wellbeing team at 0800 368 5819"


"""
test_process_recommendation_negative tests the process_recommendation function to check that the user does not receive a 
congratulatory message or support message when the predicted mood is not in the MOOD_LIST []. 
"""
def test_process_recommendation_negative():
    pass


"""
test_is_positive_mood_positive tests the is_positive_mood function to check that it returns False when a negative
mood contained in the negative_moods list is input as the predicted_mood parameter. 
"""
def test_is_positive_mood_positive():
    predicted_mood = "Sad"
    assert is_positive_mood(predicted_mood) is False


"""
test_is_positive_mood_negative tests the is_positive_mood function to check that it returns a ValueError when an unknown 
mood not contained in the positive_moods or negative_moods list is input as the predicted_mood parameter. 
"""
def test_is_positive_mood_negative():
    predicted_mood = "Disappointed"
    with pytest.raises(ValueError) as e:
        is_positive_mood(predicted_mood)
    assert str(e.value) == "Invalid mood."


"""
test_create_message_positive tests the is_positive_mood function to check that it returns the intended message when a 
negative mood is input as the predicted_mood parameter. 
"""
def test_create_message_positive():
    with patch('app.controller.is_positive_mood') as mock_is_positive_mood:
        mock_is_positive_mood.return_value = False
        result = create_message("Sad")
        assert result == ("It seems you're experiencing a challenging mood. Consider these suggestions "
                          "and feel free to seek additional support.")


"""
test_create_message_negative tests the is_positive_mood function to check that it returns a ValueError when an unknown
mood not contained in the positive_moods or negative_moods list is input as the predicted_mood parameter. 
"""
def test_create_message_negative():
    with pytest.raises(ValueError):
        create_message("Disappointed")


"""
test_retrieve_support_positive mocks a SupportService instance and also mocks the return values for the getSupportContacts()
and externalUniWellBeing() functions, which are called within the retrieve_support() function. 
"""
def test_retrieve_support_positive():
    mock_user = MagicMock()
    mock_user.id = 111

    with patch('app.controller.SupportService') as mockSupportService:
        mock_support_service = mockSupportService.return_value
        mock_support_service.getSupportContacts.return_value = "Consider contacting your emergency contact: John Doe, 123456789"
        mock_support_service.externalUniWellBeing.return_value = "Please consider contacting your University Wellbeing team at 0800 368 5819"

        contacts, wellbeing = retrieve_support(mock_user)

        assert contacts == "Consider contacting your emergency contact: John Doe, 123456789"
        assert wellbeing == "Please consider contacting your University Wellbeing team at 0800 368 5819"


"""
test_retrieve_support_negative ensures that a ValueError is raised if retrieve_support is called with an invalid parameter 
(the test function uses a user with no user.id). 
"""
def test_retrieve_support_negative():
    mock_user = MagicMock()
    mock_user.id = None

    with patch('app.controller.SupportService') as mockSupportService:
        with pytest.raises(ValueError):
            retrieve_support(mock_user)
