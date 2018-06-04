from django import forms
from .models import Course,Lesson

class CourseTest(forms.ModelForm):
    class Meta:
        model = Course
        fields=("title","overview")

class CreatedCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title","overview")

class CreateLessForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields=["course","title","video","description","attach"]

    def __init__(self,user,*args,**kwargs):
        super(CreateLessForm,self).__init__(*args,**kwargs)
        self.fields['course'].queryset=Course.objects.filter(user=user)