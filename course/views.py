from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView,DeleteView,UpdateView,View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import redirect
from .forms import CreatedCourseForm,CreateLessForm
from .models import Course,Lesson

# Create your views here.


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin,self).get_queryset()
        return qs.filter(user=self.request.user)

#------------登录重定向----------------------
class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = "/account/login"

class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = "course/manage/manage_course_list.html"

class CreatedCourseView(UserCourseMixin,CreateView):
    fields = ["title","overview"]
    template_name = "course/manage/create_course.html"

    def post(self, request, *args, **kwargs):
        form = CreatedCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})

#--------------------删除课程-------------------------------------
class DeleteCourseView(UserCourseMixin,DeleteView):
    template_name = "course/manage/delete_course_confirm.html"
    success_url = reverse_lazy("course:manage_course")

#----------------------------更新课程------------------------------------
class CourseUpdateView(UserCourseMixin,UpdateView):
    template_name = "course/manage/course_update_form.html"
    success_url = reverse_lazy("course:manage_course")
    form_class = CreatedCourseForm

#------------------------发视频-----------------------------------------
class CreateLessonView(LoginRequiredMixin,View):
    model = Lesson
    login_url = 'account/login'

    def get(self,request,*args,**kwargs):
        form = CreateLessForm(user=self.request.user)
        return render(request,"course/manage/create_lesson.html",{"from":form})

    def post(self,request,*args,**kwargs):
        form = CreateLessForm(self.request.user,request.POST,request.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user=self.request.user
            new_lesson.save()
            return redirect("course:manage_course")

#------------------------查看课题下的课件----------------------------------------
class ListLessonsView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = 'account/login'
    template_name = "course/manage/list_lessons.html"

    def get(self,request,course_id):
        course = get_object_or_404(Course,id=course_id)
        return self.render_to_response({"course":course})
#----------------------------查看课件的详细内容---------------------------------------------
class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = 'account/login'
    template_name = "course/manage/detail_lesson.html"

    def get(self,request,lesson_id):
        lesson=get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({"lesson":lesson})

#----------------------记录课程学习情况--------------------------------------------
class StudentListLessonView(ListLessonsView):
    template_name = "course/slist_lessons.html"

