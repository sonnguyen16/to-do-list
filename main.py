from flask import Flask, render_template, flash, session, redirect, request
from forms import SignupForm, SignInForm, TaskForm, ProjectForm
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
    status = db.session.query(models.Status).all()
    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        projects = db.session.query(models.Projects).filter_by(user_id = user_id).all()
        return render_template('index.html', user = user, status = status, projects = projects)
    return redirect('/')

@app.route('/home/search', methods = ['GET'])
def search():
    st = request.args.get('status')
    name = request.args.get('name')
    user_id = session.get('user_id')
    status = db.session.query(models.Status).all()
    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        if st != "0" and name != "":
            projects = db.session.query(models.Projects).filter(models.Projects.user_id == user_id, models.Projects.status_id == st, models.Projects.name.like("%" + name + "%")).all()
        elif st != "0":
            projects = db.session.query(models.Projects).filter(models.Projects.user_id == user_id, models.Projects.status_id == st).all()
        elif name != "":
            projects = db.session.query(models.Projects).filter(models.Projects.user_id == user_id, models.Projects.name.like("%" + name + "%")).all()
        else:
            projects = db.session.query(models.Projects).filter_by(user_id = user_id).all()
        return render_template('index.html', user = user, status = status, projects = projects)
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

@app.route('/edit_task', methods = ['GET', 'POST'])
def editTask():
    user_id = session.get('user_id')
    form = TaskForm()
    form.status.choices = [(s.status_id, s.desc) for s in db.session.query(models.Status).all()]
    form.priority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    form.project.choices = [(p.project_id, p.name) for p in db.session.query(models.Projects).filter_by(user_id = user_id).all()]

    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        task_id = request.form['id']
        if task_id:
            task = db.session.query(models.Task).filter_by(task_id = task_id).first()
            form.description.data = task.description
            form.deadline.data = task.deadline
            form.status.data = task.status.status_id
            form.priority.data = task.priority.priority_id
            form.project.data = task.project.project_id
            return render_template('store_task.html', user = user, form = form, task = task)
    return redirect('/')


# Route add and edit project
@app.route('/new_task', methods = ['GET','POST'])
def newTask():
    user_id = session.get('user_id')
    form = TaskForm()
    form.status.choices = [(s.status_id, s.desc) for s in db.session.query(models.Status).all()]
    form.priority.choices = [(p.priority_id, p.text) for p in db.session.query(models.Priority).all()]
    form.project.choices = [(p.project_id, p.name) for p in db.session.query(models.Projects).filter_by(user_id = user_id).all()]

    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()

        if form.validate_on_submit():
            description = form.description.data
            deadline = form.deadline.data
            status_id = form.status.data
            status = db.session.query(models.Status).filter_by(status_id = status_id).first()
            priority_id = form.priority.data
            priority = db.session.query(models.Priority).filter_by(priority_id = priority_id).first()
            project_id = form.project.data
            project = db.session.query(models.Projects).filter_by(project_id = project_id).first()

            task_id = request.form['id']
            if (task_id == "0") :
                if (project.deadline < deadline):
                    flash('Deadline must be before project deadline', 'danger')
                    return render_template('store_task.html', user = user, form = form)
                task = models.Task(description = description, deadline = deadline, status = status, priority = priority, project = project)
                if(task.status.status_id > 1 and project.status.status_id == 1):
                    project.status_id = 2
                db.session.add(task)
            else :
                task = db.session.query(models.Task).filter_by(task_id = task_id).first()
                if (project.deadline < deadline):
                    form.description.data = task.description
                    form.deadline.data = task.deadline
                    form.status.data = task.status.status_id
                    form.priority.data = task.priority.priority_id
                    form.project.data = task.project.project_id
                    flash('Deadline must be before project deadline', 'danger')
                    return render_template('store_task.html', user = user, form = form, task = task)
                if(task.status.status_id > 1 and project.status.status_id == 1):
                    project.status_id = 2

                # When all tasks in the project are completed, the project status is automatically move to completion.
               
                task.description = description
                task.deadline = deadline
                task.status = status
                task.priority = priority
                task.project = project
            
            db.session.commit()
            if db.session.query(models.Task).filter(models.Task.project_id == project_id, models.Task.status_id.in_([1, 2])).count() == 0:
                project.status_id = 3
                db.session.commit()
            else:
                project.status_id = 2
                db.session.commit()
            return redirect('/home')
        
        return render_template('store_task.html', user = user, form = form)
    return redirect('/')

@app.route('/delete_task/', methods = ['POST'])
def deleteTask():
    user_id = session.get('user_id')
    if user_id:
        task_id = request.form['id']
        task = db.session.query(models.Task).filter_by(task_id = task_id).delete()
        db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/complete_task/', methods = ['POST'])
def completeTask():
    user_id = session.get('user_id')
    if user_id:
        task_id = request.form['id']
        task = db.session.query(models.Task).filter_by(task_id = task_id).first()
        status = db.session.query(models.Status).filter_by(status_id = 3).first()
        task.status = status
        db.session.commit()
        project = db.session.query(models.Projects).filter_by(project_id = task.project.project_id).first()
        if db.session.query(models.Task).filter(models.Task.project_id == project.project_id, models.Task.status_id.in_([1, 2])).count() == 0:
            project.status_id = 3
            db.session.commit()
        else:
            project.status_id = 2
            db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/edit_project', methods = ['GET', 'POST'])
def editProject():
    user_id = session.get('user_id')
    form = ProjectForm()
    form.status.choices = [(s.status_id, s.desc) for s in db.session.query(models.Status).all()]

    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()
        project_id = request.form['id']
        if project_id:
            project = db.session.query(models.Projects).filter_by(project_id = project_id).first()
            form.name.data = project.name
            form.description.data = project.desc
            form.deadline.data = project.deadline
            form.status.data = project.status.status_id
            return render_template('store_project.html', user = user, form = form, project = project)
    return redirect('/')


# Route add and edit project
@app.route('/new_project', methods = ['GET','POST'])
def newProject():
    user_id = session.get('user_id')
    form = ProjectForm()
    form.status.choices = [(s.status_id, s.desc) for s in db.session.query(models.Status).all()]

    if user_id:
        user = db.session.query(models.User).filter_by(user_id = user_id).first()

        if form.validate_on_submit():
            desc = form.description.data
            name = form.name.data
            deadline = form.deadline.data
            status_id = form.status.data
            status = db.session.query(models.Status).filter_by(status_id = status_id).first()

            project_id = request.form['id']
            if (project_id == "0") :
                project = models.Projects(name = name, desc = desc, deadline = deadline, status = status, user = user)
                db.session.add(project)
            else :
                project = db.session.query(models.Projects).filter_by(project_id = project_id).first()
                project.name = name
                project.desc = desc
                project.deadline = deadline
                project.status = status
                project.user = user
            
            db.session.commit()
            return redirect('/home')
        
        return render_template('store_project.html', user = user, form = form)
    return redirect('/')

@app.route('/delete_project/', methods = ['POST'])
def deleteProject():
    user_id = session.get('user_id')
    if user_id:
        project_id = request.form['id']
        project = db.session.query(models.Projects).filter_by(project_id = project_id).delete()
        db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/complete_project/', methods = ['POST'])
def completeProject():
    user_id = session.get('user_id')
    if user_id:
        project_id = request.form['id']
        project = db.session.query(models.Projects).filter_by(project_id = project_id).first()
        status = db.session.query(models.Status).filter_by(status_id = 3).first()
        project.status = status
        db.session.commit()
        return redirect('/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)