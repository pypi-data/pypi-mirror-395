#!/usr/bin/python3

class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"


courses = [
    Course("Introduccion a linux", 15, "https://www.youtube.com/watch?v=iYLEJfOUiOs"),
    Course("Personalizacion de linux", 3, "https://www.youtube.com/watch?v=iYLEJfOUiOs"),
    Course("Introduccion al hacking", 53, "https://www.youtube.com/watch?v=iYLEJfOUiOs")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course
    return None

