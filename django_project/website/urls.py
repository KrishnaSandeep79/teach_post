from django.urls import path
from . import views
from . views import QuestionListView, QuestionDetailView, QuestionCreateView, QuestionUpdateView, QuestionDeleteView, UserQuestionListView, AnswerCreateView, AnswerListView, QuestionAnswerListView, SubjectListView, TeacherView, SearchView, RequestedView, AnswerDetailView, AnswerUpdateView, AnswerDeleteView


urlpatterns = [
    path('', QuestionListView.as_view(),name='index'),
    path('search/', SearchView.as_view(), name='search-index'),
    path('requested/', RequestedView.as_view(), name='requested'),
    path('request/', views.request_teacher, name='request'),
    path('user/<str:username>/', UserQuestionListView.as_view(), name='user-questions'),
    path('teacher/request/', TeacherView.as_view(), name='teacher-request'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='detail'),
    path('answer/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('question/new/', QuestionCreateView.as_view(), name='create'),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(), name='update'),
    path('answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer-update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete'),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer-delete'),
    path('about/', views.about, name='about'),
    #path('answer/<int:pk>/upvote/', UpvoteAnswer.as_view(), name='upvote'),
    #path('answer/', AnswerListView.as_view(),name='answer'),
    path('answer/new/<int:pk>/', AnswerCreateView.as_view(), name='answer-new'),
    path('answer/question/<int:pk>/', QuestionAnswerListView.as_view(), name='question-answer'),
    path('sidebar/<str:subject>/', SubjectListView.as_view(),name='sidebar')
]
