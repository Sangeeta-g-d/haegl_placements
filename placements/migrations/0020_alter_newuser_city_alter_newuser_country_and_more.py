# Generated by Django 4.2.6 on 2024-04-04 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0019_rename_company_id_id_scheduleinterview_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='city',
            field=models.CharField(default='city', max_length=100),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='country',
            field=models.CharField(default='country', max_length=300),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='linkedin',
            field=models.CharField(default='linkedin url', max_length=400),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='phone_no',
            field=models.CharField(default='contact no', max_length=100),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='state',
            field=models.CharField(default='state', max_length=300),
        ),
    ]