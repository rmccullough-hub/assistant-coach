# Generated by Django 3.1.4 on 2021-01-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_player_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image_path',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
