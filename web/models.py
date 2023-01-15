import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.conf import settings
from .LabelDecoder import decode_label_detail
from docx import Document
from docx.shared import Inches

from .managers import UserManager

class Article(models.Model):
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.number

class Record(models.Model):
    date = models.DateTimeField()
    visited = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.date

class CorrectionalWork(models.Model):
    type = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class User(AbstractUser):
    username = None
    is_admin = models.BooleanField(default=False)
    is_prisoner = models.BooleanField(default=False)
    email = models.EmailField( ('email address'), unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name.join(self.last_name)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    rank = models.CharField(max_length=45)
    gender = models.PositiveSmallIntegerField(null=True)
    birthday = models.DateField(null=True)

class Prisoner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    gender = models.PositiveSmallIntegerField()
    birthday = models.DateField()
    admin_id = models.ForeignKey(
        Admin,
        on_delete = models.CASCADE
    )
    records = models.ManyToManyField(
        Record
    )
    articles = models.ManyToManyField(
        Article
    )
    correctional_works = models.ManyToManyField(
        CorrectionalWork,
        through='PrisonerHasCorrectionalWork'
    )

class Meeting(models.Model):
    meetingcol = models.CharField(max_length=45)
    date = models.DateTimeField()
    theme = models.CharField(max_length=100)
    admin_id = models.ForeignKey(
        Admin,
        on_delete = models.CASCADE
    )
    prisoner_id = models.ForeignKey(
        Prisoner,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.theme

class PrisonerHasCorrectionalWork(models.Model):
    date = models.DateField()
    prisoner_id = models.ForeignKey(
        Prisoner,
        on_delete = models.CASCADE
    )
    correctional_work_id = models.ForeignKey(
        CorrectionalWork,
        on_delete = models.CASCADE
    )
    admin_id = models.ForeignKey(
        Admin,
        on_delete = models.CASCADE
    )
