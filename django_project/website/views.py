from django.shortcuts import render, redirect, get_object_or_404
from . models import Question, Answer
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import User
from . forms import TeacherRequestForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.decorators import teacher_required, student_required
from django.contrib import messages
from django.core.mail import send_mail

'''class UpvoteAnswer(ListView):

    def get_queryset(self):
        answer = get_object_or_404(Answer, pk=self.kwargs.get('pk'))
        answer.upvotes += 1
        answer.save()
        return answer '''


class SearchView(ListView):
    model = Question
    template_name = 'website/index.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 8

    def get_queryset(self):
        question = Question.objects.all()
        query = self.request.GET.get('search')
        if query:
            question = question.filter(question_text__icontains=query)
        return question


@login_required
@student_required
def request_teacher(request):
    if request.method == 'POST':
        form = TeacherRequestForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            teachers = filter(lambda t: t[0] in form.cleaned_data['teachers'], form.fields['teachers'].choices)
            s=""
            email_list = []
            user = User.objects.all()
            for teacher in teachers:
                s=s+teacher[1]+","
                u=user.filter(username=teacher[1])
                email_list.append(u.first().email)
                
            s=s[:-1]
            form.instance.teachers= s    
            form.save()
            send_mail("Teach Post", "Hey, "+"You got a request from your student"+request.user.username+". Please visit our website to answer the question!! http://127.0.0.1:8000/" , request.user.email, email_list)
            
            messages.success(request, f'Your question has been posted successfully!')
            return redirect('index')


    else:
        form = TeacherRequestForm()

    return render(request, 'website/teacher_request.html', {'form': form})
    
class QuestionListView(ListView):
    model = Question
    template_name = 'website/index.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 8
    def get_queryset(self):
        return Question.objects.filter(teachers="none").order_by('-date_created')

class QuestionDetailView(DetailView):
    model = Question

class AnswerDetailView(DetailView):
    model = Answer   

@method_decorator([login_required, student_required], name='dispatch')
class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question    
    fields = ['subject','question_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question    
    fields = ['subject','question_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

class UserQuestionListView(ListView):
    model = Question
    template_name = 'website/user_questions.html'
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Question.objects.filter(author=user).order_by('-date_created')


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False
    
def about(request):
    return render(request, 'website/about.html')


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text']


    def form_valid(self, form):
        q = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.question = q
        return super().form_valid(form)

class AnswerListView(ListView):
    model = Answer
    template_name = 'website/answer.html'
    context_object_name = 'answers'
    ordering = ['-answered_at']
    paginate_by = 8 

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer   
    fields = ['answer_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    success_url = '/'

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.author:
            return True
        return False

class QuestionAnswerListView(ListView):
    model = Answer
    template_name = 'website/question_answer.html'
    context_object_name = 'answers'
    paginate_by = 8

    def get_queryset(self):
        q = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        return Answer.objects.filter(question=q).order_by('-answered_at')

class SubjectListView(ListView):
    model = Question
    template_name = 'website/subject.html' 
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
        s = self.kwargs.get('subject')
        return Question.objects.filter(subject=s).order_by('-date_created')     


@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'website/teacherview.html'
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
         question = Question.objects.exclude(teachers="none")
         name_list=[]
         for q in question:
             flag=0
             name_list = q.teachers.split(",")
             for uname in name_list:
                 if self.request.user.username == uname:
                     flag=1

             if flag==0:
                 question = question.exclude(teachers=q.teachers)

         return question.order_by('-date_created')                


class RequestedView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'website/teacherview.html'
    context_object_name = 'questions'
    paginate_by = 8
    
    def get_queryset(self):
        question = Question.objects.exclude(teachers="none")
        return question.filter(author=self.request.user).order_by('-date_created') 


    