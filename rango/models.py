from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=128, unique= True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Catagory, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class Page(models.Model):
    catagory = models.ForeignKey(Catagory, on_delete= models.DO_NOTHING)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #This line is rewquired, link User Profile to a user model instance
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    #the additional attributed we want to include 
    website= models.URLField(blank=True)
    picture= models.ImageField(upload_to='profile_images', blank=True)

    #override the un __unicode__() method to return something meaningful
    def __str__(self):
        return self.user.username