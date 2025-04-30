from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, login_required
from app import app, db
from app.models import User, Mood_DB
from app.forms import ChooseForm, JournalForm
from app.controller import process_log_mood, process_journal, process_prediction, DistressAlert, process_recommendation
import sqlalchemy as sa
from datetime import datetime

"""
For the prototype, we do not include a login feature. As such we have created a user elsewhere (using hardcoded values)
and will automatically login this user upon running the app.
"""
@app.before_request
def auto_login_sample_user():
    if not current_user.is_authenticated:
        sample_user = db.session.scalar(sa.select(User).limit(1))
        if sample_user:
            login_user(sample_user)

@app.route('/')
def home():
    return render_template('home.html', title="Home")

"""
Simulates it being 6pm for a mood logging to occur
"""
@app.route('/simulate_6pm')
@login_required
def simulate_6pm():
    session['simulate_6pm'] = True
    flash("Simulation mode: It's now considered past 6pm", "info")
    return redirect(url_for('log_mood'))

"""
Simulates it being 8am for a mood prediction to occur
"""
@app.route('/simulate_8am')
@login_required
def simulate_8am():
    session['simulate_8am'] = True
    flash("Simulation mode: It's now considered past 8am", "info")
    return redirect(url_for('predict'))

"""
Upon loading the app, we check if its past 6pm or past 8am in order to provide a prediction or a mood log.
"""
@app.before_request
def require_mood_logging():
    if current_user.is_authenticated:
        cutoff_time = datetime.strptime("18:00", "%H:%M").time()
        current_time = datetime.now().time()
        eight_am = datetime.strptime("08:00", "%H:%M").time()
        today = datetime.now().date()
        #check if past 6pm
        if current_time >= cutoff_time:
            today = datetime.now().date()
            mood_entry = Mood_DB.query.filter_by(user_id=current_user.id, date=today).first()
            #check if mood has been logged today already
            if not mood_entry and request.endpoint != 'log_mood':
                flash("Please log your mood after 6pm to continue using the app.", "warning")
                return redirect(url_for('log_mood'))
        #check if past 8am and if prediction has already been shown
        if current_time >= eight_am and session.get('prediction_shown') != str(today):
            if request.endpoint != 'predict':
                return redirect(url_for('predict'))

"""
form for logging mood and redirects to journal after completion 
"""
@app.route('/log_mood', methods=['GET', 'POST'])
@login_required
def log_mood():
    form = ChooseForm()
    if request.method == 'POST' and form.validate_on_submit():
        mood = request.form.get('choice')
        if not mood:
            flash("Please select a mood.", "warning")
            return redirect(url_for('log_mood'))
        # Delegate business logic to the controller
        mood_record = process_log_mood(mood, current_user)
        session['mood_id'] = mood_record.id
        return redirect(url_for('journal'))
    return render_template('log_mood.html', title="Select Mood", form=form)

"""
Journal form is optional as described in assignment 1, redirects to distress alert if necessary
Note the activity diagram 3.2.1 in assignment 1 is incorrect as we do not view and act on suggestions or provide feedback
at this stage . This is not specified in the functional requirements and was incorrectly added to the activity diagram.
"""
@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    mood_id = session.get('mood_id')
    #checks if mood has been input (failsafe)
    if not mood_id:
        flash("No mood entry found to update.", "warning")
        return redirect(url_for('home'))
    form = JournalForm()
    if request.method == 'POST':
        #If cancel button is pressed, redirect to home and removes knowledge of mood_id input
        if form.cancel.data:
            flash("Journal form closed. No sentiment score saved.", "info")
            # Check for distress alert NOTE this is intentionally placed to only occur if the journal was filled out. This is because we only redirect when the last 7 entries have negative mood or last 7 entries have negative sentiment score.
            db_record = Mood_DB.query.get(mood_id)
            alert = DistressAlert(user_id=current_user.id)
            if alert.triggerAlert(db_record):
                flash("Your recent mood entries are consistently negative. Redirecting to distress page.", "warning")
                return redirect(url_for('distress'))
            session.pop('mood_id', None)
            return redirect(url_for('home'))
        if form.submit.data and form.validate_on_submit():
            journal_text = form.journal.data
            # Delegate journaling logic to the controller
            mood_entry, error = process_journal(mood_id, journal_text, current_user)
            if error:
                flash(error, "warning")
            else:
                flash(f"Sentiment score: {mood_entry.sentiment_score}", "success")
                flash("Sentiment score saved!", "success")
                # Check for distress alert NOTE this is intentionally placed to only occur if the journal was filled out. This is because we only redirect when the last 7 entries have negative mood or last 7 entries have negative sentiment score.
                db_record = Mood_DB.query.get(mood_id)
                alert = DistressAlert(user_id=current_user.id)
                if alert.triggerAlert(db_record):
                    flash("Your recent mood entries are consistently negative. Redirecting to distress page.", "warning")
                    return redirect(url_for('distress'))
            session.pop('mood_id', None)
            return redirect(url_for('home'))
    return render_template('journal.html', title="Optional Journal", form=form)

"""
Route for distress page, using contact emergency support.
"""
@app.route('/distress')
@login_required
def distress():
    alert = DistressAlert(user_id=current_user.id, message="Multiple negative mood entries detected!")
    mood_record = None
    if 'mood_id' in session:
        mood_record = Mood_DB.query.get(session.get('mood_id'))
    if mood_record and alert.triggerAlert(mood_record):
        alert.contactEmergencySupport()
    return render_template('distress.html', title="Distress")

"""
For prototype allows us to view all the data in the database.
"""
@app.route('/data')
@login_required
def data():
    all_entries = Mood_DB.query.filter_by(user_id=current_user.id).order_by(Mood_DB.date.desc()).all()
    return render_template('data.html', title="All Mood Entries", entries=all_entries)

"""
Route for prediction. Using controller function.
"""
@app.route('/predict')
@login_required
def predict():
    # Delegate prediction logic to the controller.
    predicted_mood = process_prediction(current_user)
    recommendation_result = process_recommendation(current_user, predicted_mood)
    if recommendation_result['support_contact']:
        flash(recommendation_result['support_contact'],"info")

    if recommendation_result['Uni_wellbeing']:
        flash(recommendation_result['Uni_wellbeing'],'info')

    session['prediction_shown'] = str(datetime.now().date())
    return render_template('predict.html', title="Prediction", predicted_mood=predicted_mood,
                           recommendation=recommendation_result)

# Error handlers remain unchanged.
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
