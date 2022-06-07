from django.db import models

# Create your models here.
# class profile(models.Model):




class Comment(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name

    def save_comment(self):
        self.save()

    def update_comment(self,name):
        Comment.objects.filter(pk=self.pk).update(name=name)

    def delete_comment(self):
        Comment.objects.filter(pk=self.pk).delete()

class Image(models.Model):
    image = models.ImageField(upload_to = 'gallery/', null=True)
    image_name = models.CharField(max_length=50)
    image_caption = models.CharField(max_length=255)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def save_image(self):
        self.save()

    def update_image(self,image_name):
        Image.objects.filter(pk=self.pk).update(image_name__image_name=image_name)

    def delete_image(self):
        Image.objects.filter(pk=self.pk).delete()

    @classmethod
    def get_image_by_id(self):
        Image.objects.get(id=self.id)

