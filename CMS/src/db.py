from unicodedata import name
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)


class Course(db.Model):
    """
    create a course class
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    code = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship("Assignment", cascade="delete")
    users = db.relationship("User", secondary = association_table, back_populates = "courses")
    users1 = db.relationship("User", secondary = association_table, back_populates = "courses")

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")
        self.assignments = []
        self.users = []
        self.users1 = []

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.users],
            "students": [s.simple_serialize() for s in self.users1]
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }

class Assignment(db.Model):
    """
    Class for an assignment
    """
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    due_date = db.Column(db.Integer, nullable = False)
    course = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", "")
        self.course_id = kwargs.get("course_id", "")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date
        }

class User(db.Model):
    """
    class for a user
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    courses = db.relationship("Course", secondary = association_table, back_populates = "users")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in self.courses] 
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid 
        }