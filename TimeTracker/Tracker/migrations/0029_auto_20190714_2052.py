# Generated by Django 2.1.8 on 2019-07-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0028_auto_20190714_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timelog',
            old_name='comment',
            new_name='end_comment',
        ),
        migrations.AddField(
            model_name='timelog',
            name='start_comment',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]
