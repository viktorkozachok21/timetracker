# Generated by Django 2.1.8 on 2019-07-14 11:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0019_timelog_spend_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
