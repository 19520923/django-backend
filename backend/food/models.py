from django.db import models
from authentication.models import User
from post.models import Post

# Create your models here


class Food(models.Model):
    name = models.CharField(max_length = 255, unique= True)
    recipe = models.TextField()
    photo = models.URLField(null = True)
    about = models.TextField(null = True, blank=True)
    avg_score = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name = 'author')
    post = models.ManyToManyField(to = Post, related_name = 'foods')
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    food = models.ForeignKey('Food', on_delete= models.CASCADE, related_name='ingredients')
    
    def __str__(self):
        return self.name
    
class FoodRate(models.Model):
    rate = models.DecimalField(max_digits=2, decimal_places= 1)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete = models.CASCADE)
    
    def __str__(self):
        return self.content

    
    
    
