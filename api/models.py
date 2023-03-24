from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Meal(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    
    def no_of_rating(self):
        rating = Rating.objects.filter(meal=self)
        return len(rating)
    
    def avg_rating(self):
        # total / len
        sum = 0
        rating = Rating.objects.filter(meal=self)
        
        for x in rating:
            sum += x.stars
        if len(rating) > 0:
            return sum / len(rating)
        else:
            return 0
    
    def __str__(self):
        return self.title
    
    
        
class Rating(models.Model):

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.user.username
    
    
    class Meal:
        unique_together = (('user', 'meal'))
        index_together = (('user', 'meal'))

    
    