from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    name = models.CharField(max_length =30)
    bio = models.TextField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile/',default ='image.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

    
    def __str__(self):
        return f'{self.user.username} profile'
    
    

class Post(models.Model):
    image = models.ImageField(upload_to = 'clone/', null=True)
    name = models.CharField(max_length=50)
    image_caption = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='user',blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='post', default='')  
    created = models.DateTimeField(auto_now_add=True,null=True)
    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE)


    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property

    def save_image(self):
        self.save()

    def update_image(self,image_name):
        Post.objects.filter(pk=self.pk).update(image_name__image_name=image_name)

    def delete_image(self):
        Post.objects.filter(pk=self.pk).delete()

    def get_all_comments(self):
        return self.comments.all()

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f'{self.user.name} Post'



class Comment(models.Model):
    body = models.TextField(default='')
    name = models.CharField(max_length=350)
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE, default='')

    def save_comment(self):
        self.save()

    def update_comment(self,name):
        Comment.objects.filter(pk=self.pk).update(name=name)

    def delete_comment(self):
        Comment.objects.filter(pk=self.pk).delete()

    def __str__(self):
        return '%s - %s' % (self.post, self.name)

