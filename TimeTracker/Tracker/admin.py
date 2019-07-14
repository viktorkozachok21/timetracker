from django.contrib import admin
from .models import Project, Task, Worker, TimeLog, Comment

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(TimeLog)
admin.site.register(Comment)
