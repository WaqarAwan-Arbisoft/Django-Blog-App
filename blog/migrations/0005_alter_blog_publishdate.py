# Generated by Django 4.0.6 on 2022-08-05 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blog_publishdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='publishDate',
            field=models.DateField(default=datetime.date(2022, 8, 5)),
        ),
    ]
