from .models import Student, ExamType, Teacher, ExamScore, Campus, Course
from django.contrib import auth
from django.contrib.auth.models import User

""" Be aware that functions in the context_processors.py file will ALWAYS return
a dictionary, if nothing is explicitly returned by you then it will return None,
this may result in a "NoneType is not iterable" error, so you must return a
dictionary, even an empty one"""

"""

DO NOT FORGET TO REGISTER YOUR CONTEXT PROCESSOR IN SETTINGS

"""


def say_hello(request):
    return {
        'say_hello': 'Hello',
    }


def course_context(request):
    """ Puts teacher specific student list into the context of every page for
    authenticated users only"""
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            teacher = request.user.teacher
            teachers = Teacher.objects.all()
            courses = Course.objects.all()
            campuses = Campus.objects.all()
            students = Student.objects.filter(teacher=teacher).order_by('last_name')
            student_count = Student.objects.filter(teacher=teacher).count()
            context = {
                'students': students,
                'student_count': student_count,
                'courses': courses,
                'campuses': campuses,
                'teachers': teachers,
                'teacher': teacher
            }
            return context
        else:
            # this is to prevent the NoneType is not iterable error
            return {}
    else:
        # this is to prevent the NoneType is not iterable error
        return {}


def exam_type(request):
    """ Creates a list of exam types for use in the 'Exam scores' dropdown in the Navbar,
    the data comes from exam types that are check for each teacher in Admin. This code only
    runs for teachers """
    if request.user.is_authenticated:
        user = request.user.id
        if Teacher.objects.filter(user__id=user).exists():
            teacher = Teacher.objects.get(user__id=user)
            exam_list = teacher.exams.values('exam_name').order_by('menu_position')
            theexams = {'exam_list': exam_list}
            return theexams
        else:
            return {}
    else:
        # this is to prevent the NoneType is not iterable error
        return {}
