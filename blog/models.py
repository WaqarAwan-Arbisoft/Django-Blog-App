from tkinter import CASCADE
from django.db import models
from datetime import date

# Create your models here.


class User(models.Model):
    username=models.CharField(max_length=30)
    fullName=models.CharField(max_length=50)
    password=models.CharField(max_length=25)
    confirmPassword=models.CharField(max_length=25)
    image=models.FileField(upload_to="images")

    def __str__(self):
        return f"Name: {self.username}, Username: {self.fullName}"




class Blog(models.Model):
    title=models.TextField()
    content=models.TextField()
    publishDate=models.DateField(default=date.today())
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.FileField(upload_to="images")

    def __str__(self):
        return f"'{self.title}' was published by {self.author.username}"


class Likes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.blog.title}' blog was liked by {self.user.username}"
