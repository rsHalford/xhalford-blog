# Generated by Django 3.1.5 on 2021-04-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210209_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]