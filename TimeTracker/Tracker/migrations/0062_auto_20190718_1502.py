# Generated by Django 2.1.10 on 2019-07-18 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0061_timelog_is_single'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timelog',
            old_name='end_comment',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='task',
            name='spend_time',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='is_single',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='spend_time',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='start_comment',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='time_of_end',
        ),
    ]
