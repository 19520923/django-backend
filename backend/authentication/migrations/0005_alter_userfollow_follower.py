# Generated by Django 4.0.2 on 2022-03-02 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_userfollow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
