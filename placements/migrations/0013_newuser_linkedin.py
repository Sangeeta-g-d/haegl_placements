# Generated by Django 4.2.6 on 2024-03-21 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0012_uploadfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='linkedin',
            field=models.CharField(default='xyz', max_length=400),
        ),
    ]