# Generated by Django 2.1.8 on 2019-07-13 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0011_auto_20190713_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracker.Worker'),
        ),
    ]
