from django.urls import path
from teacher import views as user_views

urlpatterns = [
    path('happyland/', user_views.happyland, name='happy-land'),
    path('error/', user_views.error, name='error-penguin'),
    path('<str:username>/', user_views.teacher_home, name='teacher-home'),
    path('<str:username>/reports/', user_views.reports, name='reports'),
    path('exam/<id>/entry/', user_views.u_or_c_exam, name='enter-scores'),
    path('<str:username>/student/<pk>/delete/', user_views.delete_student, name='delete-student'),
    path('<str:username>/exams/<str:exam_name>/', user_views.exam_scores, name='exam-scores'),
    path('<str:username>/student/<pk>/', user_views.StudentDetail, name='student-detail'),
    path('student/<pk>/report-mid/pdf/', user_views.render_midpdf_view, name='report-mid'),
    path('student/<pk>/report-end/pdf/', user_views.render_endpdf_view, name='report-end'),
]
