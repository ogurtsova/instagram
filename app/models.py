from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    image = models.ImageField(upload_to='upload')
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post = models.ForeignKey(Post)

class Profile(models.Model):
    userpic = models.ImageField(upload_to='upload')
    user = models.OneToOneField(User)