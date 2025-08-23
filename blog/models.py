from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Post(BaseModel):

    POST_STATUS_CHOICES = [
        ('drf','Draft'),
        ('pub','Published'),
        ('arch','Archived'),
    ]

    title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(null=True,blank=True)
    body = CKEditor5Field('Text',config_name='extends',null=True,blank=True)
    cover_image = models.ImageField(null=True,blank=True,upload_to='blog_post_covers')
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='posts',verbose_name='author')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,related_name='posts',null=True,blank=True)
    status = models.CharField(max_length=5,choices=POST_STATUS_CHOICES,default='drf')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(BaseModel):

    #TD: no hardcoding for comment variables

    COMMENT_STATUS_CHOICES = [
        ('w','Waiting'),
        ('a','Approved'),
        ('na','Not Approved'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments',verbose_name='commenter')
    title = models.CharField(max_length=50,null=True,blank=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    text = models.CharField(max_length=500,null=True,blank=True)
    status = models.CharField(max_length=5,choices=COMMENT_STATUS_CHOICES,default='w')

    def __str__(self):
        return self.title

class Like(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts_likes')
    post=  models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','post'], name='unique_like_for_every_user'
            )
        ]
