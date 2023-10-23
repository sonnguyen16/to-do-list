from main import db
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(64), index = True, nullable=False)
    last_name = db.Column(db.String(64), index = True, nullable=False)
    email = db.Column(db.String(120), index = True, unique = True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
   
    projects = db.relationship('Projects', back_populates='user')

    def __repr__(self):
        return '<User full name: {} {} , email: {}>'.format(self.first_name, self.last_name, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    
class Task(db.Model):
    task_id = db.Column(db.Integer, Sequence('task_id_seq'), primary_key=True)
    description = db.Column(db.String(255), index = True, nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    
    priority_id = db.Column(db.Integer, db.ForeignKey('priority.priority_id'))
    priority = db.relationship('Priority', back_populates='tasks')

    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=True)
    status = db.relationship('Status', back_populates='tasks')

    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=True)
    project = db.relationship('Projects', back_populates='tasks')
    
    def __repr__(self):
        return '<Task id: {} , description: {}>'.format(self.task_id, self.description)
    
class Priority(db.Model):
    priority_id = db.Column(db.Integer, Sequence('priority_id_seq'), primary_key=True)
    text = db.Column(db.String(64), nullable=False)

    tasks = db.relationship('Task', back_populates='priority')
    
    def __repr__(self):
        return '<Priority: {} , with: {}>'.format(self.priority_id, self.text)
    
class Status(db.Model):
    status_id = db.Column(db.Integer, Sequence('status_id_seq'), primary_key=True)
    desc = db.Column(db.String(64), nullable=False)

    tasks = db.relationship('Task', back_populates='status')
    projects = db.relationship('Projects', back_populates='status')
    
    def __repr__(self):
        return '<Status: {} , with: {}>'.format(self.status_id, self.text)

class Projects(db.Model):
    project_id = db.Column(db.Integer, Sequence('project_id_seq'), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.Date, nullable=False)

    tasks = db.relationship('Task', back_populates='project')

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='projects')

    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=False)
    status = db.relationship('Status', back_populates='projects')
    
    
    def __repr__(self):
        return '<Project: {} , with: {}>'.format(self.project_id, self.name)
    

    
    
    