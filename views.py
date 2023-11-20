from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from create_app import db
from model import Report


views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html', user=current_user)


@views.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        location = request.form.get('location')
        date_created = request.form.get('date_created')
        
        if len(title) < 1:
            flash('Title is too short.', category='error')
        elif len(content) < 1:
            flash('Content is too short.', category='error')
        elif len(location) < 1:
            flash('Location is too short.', category='error')
        else:
            new_report = Report(title=title, content=content, location=location, date_created=date_created, author=current_user.id)
            db.session.add(new_report)
            db.session.commit()
            flash('Report added!', category='success')
            return redirect(url_for('views.home'))
    return render_template('form.html', user=current_user, reports=reports)
