# Generated by Django 3.1 on 2020-12-31 23:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20201231_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Mark',
        ),
    ]
