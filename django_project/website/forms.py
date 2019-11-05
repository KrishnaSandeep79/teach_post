from django import forms
#from django_select2.forms import Select2MultipleWidget
from users.models import User
from . models import Question

def return_teachers():
    teachers = User.objects.all()
    t=()

    for teacher in teachers:
        if teacher.is_teacher:
            t=t+((teacher.username,teacher.username),)

    return t

class TeacherRequestForm(forms.ModelForm):
    teachers = forms.MultipleChoiceField(choices=return_teachers(), widget=forms.CheckboxSelectMultiple(), required=True)
    
    class Meta:
        model = Question
        fields = ["subject", "question_text", "teachers"]