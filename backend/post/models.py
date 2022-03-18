from django.db import models

from authentication.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    num_heart = models.IntegerField(default=0)
    author = models.ForeignKey(to = User, on_delete=models.CASCADE)
    location = models.TextField(null = True, blank=True)
    is_public = models.BooleanField(default = True)

    class Meta:
        ordering = ['-num_heart', '-create_at']
        
class Reaction(models.Model):
    post = models.ForeignKey(to =Post, on_delete= models.CASCADE, related_name='reactions')
    author = models.ForeignKey(to = User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ['-create_at']

class Photo(models.Model):
    post = models.ForeignKey(to = Post, on_delete = models.CASCADE, related_name = 'photos')
    url = models.TextField(null = True, blank = True)
    
    def __str__(self) -> str:
        return self.url
    
    
class PostComment(models.Model):
    author = models.ForeignKey(to = User, on_delete = models.CASCADE)
    post = models.ForeignKey(to = Post, on_delete = models.CASCADE, related_name = 'comments')
    create_at = models.DateTimeField(auto_now_add= True)
    content = models.TextField()
    parent = models.ForeignKey('self', related_name = 'childrent', on_delete = models.CASCADE, null=True)
    
    def __str__(self):
        return self.content
        