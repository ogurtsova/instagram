from django.db import models

class Post(models.Model):
    image = models.ImageField(upload_to='upload')
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
