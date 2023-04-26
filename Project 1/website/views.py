from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, NoteName, EventSignup

from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
# users should be logged in to view the home page
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/events', methods=['GET', 'POST'])
# users should be logged in to view the home page
@login_required
def events():

    return render_template("events.html")


@views.route('/event-signup', methods=['GET', 'POST'])
def event_signup_page():
    if current_user.is_authenticated:
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            phone = request.form['phone']
            email = request.form['email']
            time = request.form['time']
            introduction = request.form['introduction']

            new_signup = EventSignup(name=name, age=age, phone=phone, email=email, time=time, introduction=introduction)

            db.session.add(new_signup)
            db.session.commit()

            flash('You have successfully signed up for the event!', 'success')

            return render_template('home.html', user=current_user)
        else:
            return render_template('event-signup.html', user=current_user)
    else:
        flash('You need to login first!', 'warning')
        return render_template('login.html')




@views.route('/note', methods=['GET', 'POST'])
# users should be logged in to view the note page
@login_required
def note():
    if request.method == 'POST': 
        note = request.form.get('note')
        note_name = request.form.get('name')

        if len(note) < 1:
            flash('Your review is too short!', category='error') 
        else:
            new_note_name = NoteName(name=note_name)
            new_note = Note(data=note, user_id=current_user.id, note_name=new_note_name)              
            #adding the note with name to the database 
            db.session.add(new_note_name)
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Your Note is recorded!', category='success')

    return render_template("note.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
