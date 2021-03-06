# Generated by Django 2.1.10 on 2019-07-18 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0065_timelog_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelog',
            name='spend_time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='post',
            field=models.CharField(blank=True, choices=[('A', 'Analyst'), ('D', 'Designer'), ('M', 'Manager'), ('T', 'Tester'), ('P', 'Programmer'), ('E', 'Engineer'), ('L', 'Lead')], default='E', max_length=1),
        ),
    ]
