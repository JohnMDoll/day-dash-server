# Generated by Django 4.1.7 on 2023-03-09 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daydashapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='friendee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friended_user', to='daydashapi.dashuser'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='friender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_friend', to='daydashapi.dashuser'),
        ),
    ]
