
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

#max of 200 characters in form as stated in FR3 functional requirement 3
class JournalForm(FlaskForm):
    journal = TextAreaField('Journal Entry', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Submit Journal')
    cancel = SubmitField('Close Form')