# Generated by Django 4.0.2 on 2022-03-02 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('food', '0004_rename_author_id_food_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='post.post'),
        ),
    ]
