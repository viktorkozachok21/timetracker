# Generated by Django 2.1.10 on 2019-07-20 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0068_comment_is_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_blocked',
        ),
        migrations.AddField(
            model_name='worker',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
