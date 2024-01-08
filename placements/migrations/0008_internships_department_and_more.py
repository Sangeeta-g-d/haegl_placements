# Generated by Django 4.1.7 on 2024-01-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0007_internships'),
    ]

    operations = [
        migrations.AddField(
            model_name='internships',
            name='department',
            field=models.CharField(default='sales', max_length=300),
        ),
        migrations.AlterField(
            model_name='internships',
            name='internship_type',
            field=models.CharField(default='Unpaid', max_length=400),
        ),
    ]
