# Generated by Django 4.2.6 on 2024-04-10 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0022_rename_profile_jobdetails_company_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetails',
            name='promoting_company_name',
            field=models.CharField(default='promoting company name', max_length=700),
        ),
    ]