# Generated by Django 3.1.1 on 2020-09-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20200928_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover_picture',
            field=models.ImageField(default='default_cover.jpg', upload_to='cover_pics/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Ma', 'Male'), ('Fe', 'Female'), ('Un-Sp', 'Rather not say')], max_length=5),
        ),
    ]
