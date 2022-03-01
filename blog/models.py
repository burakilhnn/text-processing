from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Pdf(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,default=None, blank=True, null=True)
    file = models.FileField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    student = models.CharField(max_length=50,default=None, blank=True, null=True)
    lesson = models.CharField(max_length=50,default=None, blank=True, null=True)
    season = models.CharField(max_length=50,default=None, blank=True, null=True)
    keywords = ArrayField(ArrayField(models.CharField(max_length=100)),default=list)
    judges = ArrayField(ArrayField(models.CharField(max_length=100)),default=list)
    supervisor = models.CharField(max_length=50,default=None, blank=True, null=True)
    summary = models.TextField(max_length=500,default=None, blank=True, null=True)
    student_no = models.IntegerField(default=None, blank=True, null=True)
    type_of_edu = models.CharField(max_length=50,default=None, blank=True, null=True)

    def __str__(self):
        return str(self.title)