# Generated by Django 2.2.3 on 2019-07-12 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='worker',
            name='avatar',
            field=models.ImageField(blank=True, choices=[('1', 'https://mdbootstrap.com/img/Photos/Avatars/avatar-1.jpg'), ('2', 'https://mdbootstrap.com/img/Photos/Avatars/avatar-2.jpg'), ('3', 'https://mdbootstrap.com/img/Photos/Avatars/avatar-3.jpg')], default='1', max_length=1, upload_to=''),
        ),
        migrations.AlterField(
            model_name='worker',
            name='post',
            field=models.CharField(blank=True, choices=[('D', 'Designer'), ('A', 'Analyst'), ('M', 'Manager'), ('D', 'Developer'), ('E', 'Engineer')], default='E', max_length=1),
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_start', models.TimeField()),
                ('time_of_end', models.TimeField()),
                ('comment', models.TextField()),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracker.Task')),
            ],
        ),
    ]
