# Generated by Django 2.1.8 on 2019-07-14 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0031_auto_20190714_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='time_of_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='time_of_start',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
