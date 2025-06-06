# Generated by Django 5.2.1 on 2025-05-20 02:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='post.post'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('content', models.CharField(max_length=255, verbose_name='내용')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('tag', models.CharField(max_length=100, verbose_name='태그')),
                ('posts', models.ManyToManyField(related_name='tags', to='post.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
