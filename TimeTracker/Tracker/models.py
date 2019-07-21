from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import uuid


class Project(models.Model):

    project_name = models.CharField(max_length=256)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = HTMLField('Summary')
    created_on = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField('Worker', help_text="Select a worker for this project", related_name='project_worker')
    is_completed = models.BooleanField(default=False)
    date_of_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_on", "is_completed"]

    def complete(self):
        self.created_on = datetime.now() - timedelta(days=7)
        self.date_of_end = datetime.now()
        self.is_completed = True
        self.save()

    def open(self):
        self.created_on = datetime.now()
        self.is_completed = False
        self.save()

    def __str__(self):
        return self.project_name


class Task(models.Model):

    title = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = CurrentUserField(editable=False)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True)
    description = HTMLField('Description')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    PRIORITIZE = (
        ('L', 'Low'),
        ('N', 'Normal'),
        ('H', 'High'),
        ('I', 'Important'),
        ('U', 'Urgent'),
    )
    priority_of_task = models.CharField(max_length=1, choices=PRIORITIZE, default='N')
    TYPES = (
        ('B', 'Bug'),
        ('F', 'Feature'),
        ('T', 'Task'),
        ('I', 'Improvement'),
    )
    type_of_task = models.CharField(max_length=1, choices=TYPES, default='T')
    date_of_start = models.DateTimeField(auto_now_add=True)
    date_of_end = models.DateTimeField(null=True, blank=True)
    available_from = models.DateField()
    available_to = models.DateField()
    is_available = models.BooleanField(default=False)
    estimated_time = models.CharField(max_length=10, default="24:00:00")
    spent_time = models.CharField(max_length=9, default="00:00:00")

    class Meta:
        ordering = ["-date_of_start", "is_completed"]

    def accessibility(self):
        today = datetime.now().date()
        if self.available_from <= today and self.available_to >= today:
            self.is_available = True
        else:
            self.is_available = False
        self.save()

    def complete(self):
        self.date_of_start = datetime.now() - timedelta(days=7)
        self.date_of_end = datetime.now()
        self.worker = None
        self.is_active = False
        self.is_completed = True
        self.save()

    def open(self):
        self.date_of_start = datetime.now()
        self.is_completed = False
        self.estimated_time = "24:00:00"
        self.spent_time = "00:00:00"
        self.save()

    def end(self):
        self.date_of_end = datetime.now()
        self.is_active = False
        self.worker = None
        self.save()

    def __str__(self):
        return self.title


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
    date_of_birth = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    date_of_start = models.DateField(auto_now_add=True)
    POSTS = (
        ('1', 'Analyst'),
        ('2', 'Designer'),
        ('3', 'Developer'),
        ('4', 'Engineer'),
        ('5', 'Lead'),
        ('6', 'Manager'),
        ('7', 'Programmer'),
        ('8', 'Tester'),
    )
    post = models.CharField(max_length=1, choices=POSTS, default='3')
    avatar = models.ImageField(default="img/default.webp", blank=True, null=True, upload_to="avatars")

    class Meta:
        ordering = ["-date_of_start", "is_blocked"]

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def full_name(self):
        return self.last_name + ' ' + self.first_name

    def block(self):
        self.is_blocked = True
        self.save()

    def unblock(self):
        self.is_blocked = False
        self.save()

class TimeLog(models.Model):

    time_of_start = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=256)
    worker = models.ForeignKey('Worker', on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    spent_time = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ["-time_of_start"]

    def __str__(self):
        return self.action

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

    def read(self):
        self.status = ""
        self.save()
