# Generated by Django 2.1.10 on 2019-07-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0074_auto_20190721_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='spend_time',
            new_name='spent_time',
        ),
        migrations.RenameField(
            model_name='timelog',
            old_name='spend_time',
            new_name='spent_time',
        ),
        migrations.AlterField(
            model_name='task',
            name='type_of_task',
            field=models.CharField(choices=[('B', 'Bug'), ('F', 'Feature'), ('T', 'Task'), ('I', 'Improvement')], default='T', max_length=1),
        ),
        migrations.AlterField(
            model_name='worker',
            name='post',
            field=models.CharField(choices=[('1', 'Analyst'), ('2', 'Designer'), ('3', 'Developer'), ('4', 'Engineer'), ('5', 'Lead'), ('6', 'Manager'), ('7', 'Programmer'), ('8', 'Tester')], default='3', max_length=1),
        ),
    ]
