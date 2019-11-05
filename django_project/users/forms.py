from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile, User, Student, Teacher
from django.db import transaction

YEAR = (('1','1'),('2','2'),('3','3'),('4','4'))
BRANCH = (('cse','CSE'),('it','IT'),('ece','ECE'),('eee','EEE'),('mech','Mech'),('civil','Civil'))
DEPARTMENT = (('maths','Maths'),('physics','Physics'),('chemistry','Chemistry'),('cse','CSE'),('it','IT'),('ece','ECE'),('eee','EEE'),('mech','Mech'),('civil','Civil'))
SUBJECTS = (('maths','Maths'),('physics','Physics'),('chemistry','Chemistry'),('cse','Computer Science'),('eee','Electronics and Electrical'),('ece','Communications'),('mech','Mechanics'))


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField()
    year = forms.ChoiceField(choices=YEAR)
    branch = forms.ChoiceField(choices=BRANCH)

    class Meta:
        model = User
        fields = ['username', 'email', 'year', 'branch', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.year = self.cleaned_data.get('year')
        student.branch = self.cleaned_data.get('branch')
        student.save()
        return user    

class TeacherRegisterForm(UserCreationForm):
    email = forms.EmailField()
    department = forms.ChoiceField(choices=DEPARTMENT)
    subject = forms.ChoiceField(choices=SUBJECTS)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'department', 'subject', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.department = self.cleaned_data.get('department')
            teacher.subject = self.cleaned_data.get('subject')
            teacher.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

