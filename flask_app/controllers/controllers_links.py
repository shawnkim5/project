from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.models_link import Art
from flask_app.models.models_user import User

from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/home')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')
    user_data = {
        'id' : session['user_id']

    }
    user = User.get_one(user_data)
    all = Art.all_arts()
    return render_template('dashboard.html', user = user, all = all)


# submit link page
@app.route('/submit_link')
def submit_link():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('submit_link.html')

# submitting link
@app.route('/create_link', methods=['POST'])
def create_art():
    if not Link.link_validator(request.form):
        return redirect('/submit_link')
    data = {
        'link' : request.form['link'],
        'user_id' : session['user_id']
    }
    Link.create_art(data)
    return redirect('/home')


