from django.db import models
from django.utils import timezone

# Create your models here.
class UserTable(models.Model):
    username = models.CharField(max_length = 10)
    e_mail = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    profile_pic = models.ImageField(upload_to = 'pics',default = 'static/main/img.png')
    bio = models.CharField(max_length = 100)
    mobile_num = models.IntegerField(default=0)
    date_of_join = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    Admin = models.BooleanField(default = False)


class UserPostTable(models.Model):
    post_id = models.CharField(max_length = 30,default = None)
    username = models.CharField(max_length = 100)
    img = models.FileField(upload_to = 'pics')
    profile_pic = models.ImageField(upload_to = 'pics')
    post_file = models.IntegerField(default = 0)
    caption = models.TextField()
    post_count = models.IntegerField(default = 0)
    tag = models.CharField(max_length = 20)   # lost_found,suggestion,problems,trending,memes/jokes,fets/club/sport,
    comments = models.TextField()
    comments_count = models.IntegerField(default = 0)
    likes = models.TextField()
    likes_count = models.IntegerField(default = 0)
    dislikes = models.TextField()
    dislikes_count = models.IntegerField(default=0)
    posted_date = models.DateTimeField(default=timezone.now)
    Admin = models.BooleanField(default = False)



