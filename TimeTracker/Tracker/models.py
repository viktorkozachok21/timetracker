from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
import uuid


class Project(models.Model):

    project_name = models.CharField(max_length=256)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = HTMLField('Summary')
    created_on = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField('Worker', help_text="Select a worker for this project")

    class Meta:
        ordering = ["-created_on"]

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

    def __str__(self):
        return self.project_name


class Task(models.Model):

    title = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True)
    summary = HTMLField('Summary')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField()
    is_completed = models.BooleanField()

    PRIORITIZE = (
        ('N', 'Normal'),
        ('H', 'High'),
        ('U', 'Urgent'),
    )

    priority_of_task = models.CharField(max_length=1, choices=PRIORITIZE, blank=True, default='N')

    TYPES = (
        ('B', 'Bug'),
        ('F', 'Feature'),
    )

    type_of_task = models.CharField(max_length=1, choices=TYPES, blank=True, default='B')
    date_of_start = models.DateField(auto_now_add=True)
    date_of_end = models.DateField(null=True, blank=True)
    estimated_time = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.project.project_name + " ~ " + self.title


class Comment(models.Model):

    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]


class Worker(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    POSTS = (
        ('D', 'Designer'),
        ('A', 'Analyst'),
        ('M', 'Manager'),
        ('T', 'Tester'),
        ('D', 'Developer'),
        ('E', 'Engineer'),
        ('L', 'Lead'),
    )

    post = models.CharField(max_length=1, choices=POSTS, blank=True, default='E')
    avatar = models.ImageField()

    def get_absolute_url(self):
        return reverse('worker-detail', args=[str(self.id)])

    def __str__(self):
        return self.last_name + ' ' + self.first_name

class TimeLog(models.Model):

    time_of_start = models.TimeField(auto_now_add=True)
    time_of_end = models.TimeField(null=True, blank=True)
    spend_time = models.TimeField(null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    def __str__(self):
        return self.task.project.project_name + " ~ " + self.task.title

    def get_end(self):
        self.time_of_end = datatime.now()
        self.spend_time = self.time_of_end - self.time_of_start
