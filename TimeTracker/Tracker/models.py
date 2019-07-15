from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField
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

    def __str__(self):
        return self.project_name


class Task(models.Model):

    title = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = CurrentUserField(editable=False)
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
    date_of_start = models.DateTimeField(auto_now_add=True)
    date_of_end = models.DateTimeField(null=True, blank=True)
    estimated_time = models.CharField(max_length=10, default="24:00:00")
    spend_time = models.CharField(max_length=10, default="00:00:00")

    class Meta:
        ordering = ["-date_of_start"]

    def complete(self):
        self.date_of_end = datetime.now()
        self.is_completed = True
        self.save()

    def open(self):
        self.date_of_start = datetime.now()
        self.is_completed = False
        self.estimated_time = "20:00:00"
        self.save()

    def spent(self, new_time):
        self.spend_time = new_time
        self.save()

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

    time_of_start = models.DateTimeField(auto_now_add=True)
    time_of_end = models.DateTimeField(null=True, blank=True)
    spend_time = models.TimeField(null=True, blank=True)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    start_comment = models.TextField()
    end_comment = models.TextField()
    is_completed = models.BooleanField()

    class Meta:
        ordering = ["-time_of_start"]

    def get_end(self):
        self.time_of_end = datetime.now()
        hour = self.time_of_end.hour - self.time_of_start.hour
        minute = self.time_of_end.minute - self.time_of_start.minute
        second = self.time_of_end.second - self.time_of_start.second
        duration_time = str(hour) + ":" + str(minute) + ":" + str(second)
        self.spend_time = duration_time
        self.save()

    def __str__(self):
        return self.task.project.project_name + " ~ " + self.task.title

class Message(models.Model):

    title = models.CharField(max_length=256)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True)
    message = HTMLField('Message')
    status = models.CharField(max_length=10, default="new", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
