# Generated by Django 3.2.6 on 2022-11-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='description',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='news',
            name='channel_name',
        ),
        migrations.RemoveField(
            model_name='news',
            name='guid',
        ),
        migrations.RemoveField(
            model_name='news',
            name='link',
        ),
        migrations.RemoveField(
            model_name='news',
            name='pub_date',
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
