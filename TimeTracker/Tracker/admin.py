from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Worker)
admin.site.register(TimeLog)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Task)
