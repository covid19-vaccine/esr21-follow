# Generated by Django 3.1.4 on 2021-10-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esr21_follow', '0002_auto_20211011_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklist',
            name='appointment_id',
            field=models.UUIDField(blank=True, default=None, editable=False),
            preserve_default=False,
        ),
    ]
