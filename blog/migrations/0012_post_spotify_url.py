# Generated by Django 5.1 on 2024-08-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='spotify_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
