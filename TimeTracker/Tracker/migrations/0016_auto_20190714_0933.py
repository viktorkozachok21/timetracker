# Generated by Django 2.1.8 on 2019-07-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0015_auto_20190713_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.CharField(max_length=10),
        ),
    ]
