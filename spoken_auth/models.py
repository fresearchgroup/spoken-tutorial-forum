from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#from drupal_auth.managers import DrupalUserManager
class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L, unique=True)
    class Meta:
        db_table = 'auth_group'

class Users(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100L, unique=True)
    email = models.CharField(max_length=100L, unique=True)
    is_active = models.BooleanField()
    groups = models.ManyToManyField(Group, related_name="user_groups", through='UserGroups')
    USERNAME_FIELD = 'username'
    class Meta:
        db_table = 'auth_user'

class UserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users)
    group = models.ForeignKey(Group)
    class Meta:
        db_table = 'auth_user_groups'

class FossCategory(models.Model):
    foss = models.CharField(unique=True, max_length = 255)
    description = models.TextField()
    status = models.BooleanField(max_length = 2)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = 'creation_fosscategory'

class Language(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = 'creation_language'

class Level(models.Model):
    level = models.CharField(max_length = 255)
    code = models.CharField(max_length = 10)

    class Meta:
        db_table = 'creation_level'

class TutorialDetails(models.Model):
    foss = models.ForeignKey(FossCategory)
    tutorial = models.CharField(max_length = 255)
    order = models.IntegerField()
    level = models.ForeignKey(Level)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'creation_tutorialdetail'

class TutorialResources(models.Model):
    id = models.IntegerField(primary_key=True)
    tutorial_detail = models.ForeignKey(TutorialDetails)
    language = models.ForeignKey(Language)
    video = models.TextField()
    status = models.PositiveSmallIntegerField(default = 0)

    class Meta:
        db_table = 'creation_tutorialresource'
