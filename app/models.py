from django.db import models

class Post(models.Model):
    image = models.ImageField(upload_to='upload')
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author_name = models.CharField(max_length=64)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    post = models.ForeignKey(Post)
