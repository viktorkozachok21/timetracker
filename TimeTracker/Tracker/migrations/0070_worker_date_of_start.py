# Generated by Django 2.1.10 on 2019-07-20 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0069_auto_20190720_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='date_of_start',
            field=models.DateField(auto_now_add=True, default='2019-07-20'),
            preserve_default=False,
        ),
    ]