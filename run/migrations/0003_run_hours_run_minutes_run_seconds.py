# Generated by Django 5.0.6 on 2024-09-22 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0002_alter_run_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='seconds',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
