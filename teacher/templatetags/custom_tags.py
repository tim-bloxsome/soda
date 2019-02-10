from django import template
from teacher.models import ExamScore, Student


register = template.Library()


@register.simple_tag
def any_function():
    count = Student.objects.count()
    return count


@register.simple_tag
def unique_exam(student_id, exam_name, skill):
    if ExamScore.objects.filter(student_id=student_id, exam_name=exam_name).exists():
        e = ExamScore.objects.get(student_id=student_id, exam_name=exam_name)
        e = getattr(e, skill, "")
        return e
    else:
        return ""
