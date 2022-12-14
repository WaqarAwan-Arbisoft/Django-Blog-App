# Generated by Django 4.0.6 on 2022-08-05 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
        ),
    ]
