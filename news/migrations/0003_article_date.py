# Generated by Django 3.1.3 on 2020-11-21 23:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.date(2020, 11, 21)),
        ),
    ]