# Generated by Django 3.1 on 2020-12-24 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20201224_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
        migrations.AlterField(
            model_name='courseinstance',
            name='slug',
            field=models.SlugField(allow_unicode=True, unique=True),
        ),
    ]