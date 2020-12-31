# Generated by Django 3.1 on 2020-12-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_mark_enroll'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalassignment',
            name='answer_field',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personalassignment',
            name='answer_files',
            field=models.FileField(blank=True, null=True, upload_to='assignments/files/'),
        ),
    ]