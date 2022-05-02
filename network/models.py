from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post =  models.CharField(null=True, max_length=300)
    date= models.DateTimeField(null=True)
    def __str__(self):
        return f"{self.post}"

class Likes(models.Model):
    post =  models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name = "likebutton")
    like = models.ManyToManyField(User, null=True)
    class Meta:
        verbose_name_plural = "Likes"
    def __str__(self):
        return f"{self.post}"

class Follows(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, null=True, related_name="followed")
    class Meta:
        verbose_name_plural = "Follows"
    def __str__(self):
        return f"{self.user}"


