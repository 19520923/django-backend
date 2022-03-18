# Generated by Django 4.0.2 on 2022-03-02 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('food', '0008_alter_food_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='post',
        ),
        migrations.AddField(
            model_name='food',
            name='post',
            field=models.ManyToManyField(related_name='foods', to='post.Post'),
        ),
    ]
