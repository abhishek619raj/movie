from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
image = "https://m.media-amazon.com/images/G/01/imdb/images-ANDW73HA/imdb_fb_logo._CB1542065250_.png"

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)


class Movie(models.Model):
    popularity = models.FloatField(blank=True)
    director = models.CharField(max_length=100,blank=True)
    genre = models.CharField(max_length=100,blank=True)
    imdb_score = models.FloatField(blank=True)
    name = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='movie_cover_photo', default='image')
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)



#this will create token for user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)