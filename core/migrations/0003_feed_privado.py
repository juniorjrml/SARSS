# Generated by Django 3.1.7 on 2021-03-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_feed_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='privado',
            field=models.BooleanField(auto_created=True, default=True),
            preserve_default=False,
        ),
    ]