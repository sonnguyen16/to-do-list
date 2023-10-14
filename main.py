from flask import Flask, render_template, flash, session, redirect
from forms import SignupForm, SignInForm, TaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/home')
def home():
    user_id = session.get('user_id')
    form = TaskForm()
    form.priority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        return render_template('index.html', user = user, form = form)
    return redirect('/')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
    
        if (db.session.query(models.User).filter_by(email = email).count() > 0):
            flash('Email already exists', 'danger')
            return render_template('signup.html', form = form)
        
        user = models.User(first_name = first_name, last_name = last_name, email = email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template('signup_success.html', user = user)
    return render_template('signup.html', form = form)

@app.route('/', methods = ['GET', 'POST'])
def main():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.query(models.User).filter_by(email = email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return render_template('signin.html', form = form)
        session['user_id'] = user.user_id
        return redirect('/home')
    return render_template('signin.html', form = form)

@app.route('/new_task', methods = ['POST'])
def newTask():
    user_id = session.get('user_id')
    form = TaskForm()
    form.priority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        if form.validate_on_submit():
            description = form.description.data
            priority_id = form.priority.data
            priority = db.session.query(models.Priority).filter_by(priority_id = priority_id).first()
            task = models.Task(description = description, user = user, priority = priority)
            db.session.add(task)
            db.session.commit()
            return redirect('/home')
        return render_template('index.html', user = user, form = form)
    
    return redirect('/')

@app.route('/edit_task/<int:task_id>', methods = ['POST'])
def editTask(task_id):
    user_id = session.get('user_id')
    form = TaskForm()
    form.priority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        if form.validate_on_submit():
            task = db.session.query(models.Task).filter_by(task_id = task_id).first()
            task.description = form.description.data
            task.priority_id = form.priority.data
            db.session.commit()
            return redirect('/home')
        return render_template('index.html', user = user, form = form)
    return redirect('/')

@app.route('/delete_task/<int:task_id>')
def deleteTask(task_id):
    user_id = session.get('user_id')
    if user_id:
        task = db.session.query(models.Task).filter_by(task_id = task_id).delete()
        db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/complete_task/<int:task_id>')
def completeTask(task_id):
    user_id = session.get('user_id')
    if user_id:
        task = db.session.query(models.Task).filter_by(task_id = task_id).first()
        task.isCompleted = True
        db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)