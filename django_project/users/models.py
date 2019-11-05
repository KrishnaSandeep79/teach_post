from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

YEAR = (('1','1'),('2','2'),('3','3'),('4','4'))
BRANCH = (('cse','CSE'),('it','IT'),('ece','ECE'),('eee','EEE'),('mech','Mech'),('civil','Civil'))
DEPARTMENT = (('maths','Maths'),('physics','Physics'),('chemistry','Chemistry'),('cse','CSE'),('it','IT'),('ece','ECE'),('eee','EEE'),('mech','Mech'),('civil','Civil'))
SUBJECTS = (('maths','Maths'),('physics','Physics'),('chemistry','Chemistry'),('cse','Computer Science'),('eee','Electronics and Electrical'),('ece','Communication'),('mech','Mechanics'))

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    class Meta:
        db_table='auth_user'

    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=1, choices=YEAR, default='none')
    branch = models.CharField(max_length=5, choices=BRANCH, default='none')

    def __str__(self):
        return f'{self.user.username} Info'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=20, choices=DEPARTMENT, default='none')
    subject = models.CharField(max_length=20, choices=SUBJECTS, default='none')

    def __str__(self):
        return f'{self.user.username} Info'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

