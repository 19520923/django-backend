# Generated by Django 4.0.2 on 2022-02-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_first_name_user_is_verified_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]