# Generated by Django 4.1.7 on 2023-03-07 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DashUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500, null=True)),
                ('location', models.CharField(max_length=500, null=True)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tags', to='daydashapi.dashuser')),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_tags', models.ManyToManyField(related_name='tagged_friends', to='daydashapi.tag')),
                ('friendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_friend', to='daydashapi.dashuser')),
                ('friender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friended_user', to='daydashapi.dashuser')),
            ],
        ),
        migrations.CreateModel(
            name='EventComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='daydashapi.dashuser')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_comments', to='daydashapi.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(related_name='event_tags', to='daydashapi.tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to='daydashapi.dashuser'),
        ),
    ]
