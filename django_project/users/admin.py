from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import Profile, Student, Teacher, User

admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Teacher)


