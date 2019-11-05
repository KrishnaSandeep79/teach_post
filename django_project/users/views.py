from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import StudentRegisterForm, TeacherRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from . models import User

def choice(request):
    return render(request, 'users/choice.html')

class StudentRegisterView(CreateView):
    model = User
    form_class = StudentRegisterForm
    template_name = 'users/student_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Your account has been created! You are now able to login')
        return redirect('login')

class TeacherRegisterView(CreateView):
    model = User
    form_class = TeacherRegisterForm
    template_name = 'users/teacher_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Your account has been created! You are now able to login')
        return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = { 
        'u_form': u_form,
        'p_form': p_form
     }
    return render(request, 'users/profile.html', context)