# Generated by Django 2.1.10 on 2019-07-17 23:45

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0058_project_date_of_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='summary',
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=tinymce.models.HTMLField(default=1, verbose_name='Description'),
            preserve_default=False,
        ),
    ]