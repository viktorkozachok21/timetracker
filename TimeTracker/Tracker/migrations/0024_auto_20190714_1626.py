# Generated by Django 2.1.8 on 2019-07-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0023_task_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
