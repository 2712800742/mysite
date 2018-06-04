from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns =[
    url(r'about/$',TemplateView.as_view(template_name="course/about.html"),name='about'),
    url(r"test/$",views.Test,name="course"),
    url(r'course_list/$',views.CourseListView.as_view(),name='course_list'),
    url(r'manage_course/$',views.ManageCourseListView.as_view(),name="manage_course"),
    url(r"create_course/$",views.CreatedCourseView,name="create_course"),
    url(r'delete-course/(?P<pk>\d+)/$',views.DeleteView.as_view(),name="delete_course"),
    url(r'update-course/(?P<pk>\d+)/$',views.CourseUpdateView.as_view(),name="update_course"),
    url(r'create-lesson/$',views.CreateLessonView.as_view(),name='create_lesson'),
    url(r'list-lessons/(?P<course_id>\d+)/$',views.ListLessonsView.as_view(),name="list_lessons"),
    url(r'detail-lesson/(?P<lesson_id>\d+)/$',views.DetailLessonView.as_view(),name="detail_lesson"),
    url(r'lesson-list/(?P<course_id>\d+)/$',views.StudentListLessonView.as_view(),name="lessons_list"),
]