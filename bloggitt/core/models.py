from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from .utils import get_read_time
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
from django.dispatch import receiver


# Create your models here.
class TagDict(models.Model):
    tag = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.tag
 

class Post(models.Model):
    CATEGORY_CHOICES = ( 
        ("1", "Programming/Technology"), 
        ("2", "Health/Fitness"), 
        ("3", "Personal"), 
        ("4", "Fashion"), 
        ("5", "Food"), 
        ("6", "Travel"), 
        ("7", "Business"), 
        ("8", "Art"),
        ("9", "Other"), 
    ) 
    
    category = models.CharField( 
        max_length = 20, 
        choices = CATEGORY_CHOICES, 
        default = '1'
        ) 
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    read_count = models.IntegerField(default=0, editable=False)
    read_time = models.IntegerField(default=0, editable=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

        for tag in self.tags.all():
            tag_dict,_ = TagDict.objects.get_or_create(tag=str(tag))
            tag_dict.count += 1
            tag_dict.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug":self.slug})

    def get_like_url(self):
        return reverse('like-toggle', kwargs={"slug":self.slug})
    
    def get_api_like_url(self):
        return reverse('like-api-toggle', kwargs={"slug":self.slug})


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        instance.read_time = get_read_time(instance.content)

pre_save.connect(pre_save_post_receiver, sender=Post)



class FavouritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    profile_image = models.ImageField(default='default.jpeg', upload_to ='profile_pics', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

