# Generated by Django 2.1.8 on 2019-07-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0018_auto_20190714_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelog',
            name='spend_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
