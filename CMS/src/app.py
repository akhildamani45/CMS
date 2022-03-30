from collections import UserString
from db import db
from db import Course
from db import User
from db import Assignment
import json
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(data, code=404):
    return json.dumps(data), code
    
@app.route("/")
@app.route("/api/courses/")
def get_courses():
    """
    Gets all courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})

@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Create course
    """
    body = json.loads(request.data)
    code = body.get("code")
    name = body.get("name")
    if not name or not code:
        return failure_response({"error":"bad request"} ,400)
    new_course = Course(code= code, name= name)
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    get specific course
    """
    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return failure_response({"error":"course not found"})
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/", methods = ["DELETE"])
def delete_course(course_id):
    """
    Delete course
    """
    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return failure_response("course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Creates users
    """
    body = json.loads(request.data)
    name = body.get("name")
    netid = body.get("netid")
    if not name or not netid:
        return failure_response({"error": "Bad request"}, 400)
    new_user = User(name = name, netid = netid)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Gets user
    """
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return failure_response({"error":"user not found"})
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Adds user to a course
    """
    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return failure_response({"error":"course not found"})
    body = json.loads(request.data)
    user_id = body.get("user_id")
    type = body.get("type")
    if not user_id or not type:
        return failure_response({"error":"bad request"})
    user = User.query.filter_by(id = user_id).first()
    course.users.append(user)
    db.session.commit()
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def create_assignment(course_id):
    """
    create assignment for a course
    """
    course = Course.query.filter_by(id = course_id).first()
    if not course:
        return failure_response({"error":"course not found"})
    body = json.loads(request.data)
    title = body.get("title")
    due_date = body.get("due_date")
    if not title or not due_date:
        return failure_response({"error":"bad request"}, 400)
    assignment = Assignment(title = title, due_date = due_date, course_id = course_id)
    db.session.add(assignment)
    course.assignments.append(assignment)
    db.session.commit()
    var = assignment.serialize()
    var["course"] = course.simple_serialize()
    return success_response(var, 201)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
