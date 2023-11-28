from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avator = models.ImageField(null=True, upload_to='profile/', default="profile/avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class PersonalChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='origin')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intended')
    message = models.TextField(null=False)
    time = models.DateTimeField(auto_now_add=True)
    statis = models.CharField(max_length=20)


class Groups(models.Model):
    founder = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="founder")
    name = models.CharField(max_length=100)
    icon = models.ImageField()
    description = models.TextField()
    rules = models.TextField()
    groupcode = models.CharField(max_length=30, unique=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    group_password = models.CharField(max_length=50)


class GroupAdmin(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='member')
    admin = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class GroupMembers(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class GroupMessages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    message = models.TextField(null=False)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
