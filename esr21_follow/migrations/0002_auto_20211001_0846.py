# Generated by Django 3.1.4 on 2021-10-01 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esr21_follow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worklist',
            name='prev_study',
        ),
        migrations.RemoveField(
            model_name='worklist',
            name='study_maternal_identifier',
        ),
    ]
