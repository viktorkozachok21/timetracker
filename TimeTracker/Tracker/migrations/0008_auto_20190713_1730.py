# Generated by Django 2.1.8 on 2019-07-13 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0007_auto_20190713_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
