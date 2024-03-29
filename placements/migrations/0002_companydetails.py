# Generated by Django 4.1.7 on 2024-01-06 07:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_line', models.CharField(default='tagline', max_length=700)),
                ('company_type', models.CharField(default='startup', max_length=100)),
                ('company_service_sector', models.CharField(default='IT Services', max_length=1000)),
                ('why_us', models.CharField(default='abcd', max_length=2000)),
                ('founded_year', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2024)])),
                ('head_branch', models.CharField(default='hubli', max_length=500)),
                ('milestone', models.CharField(default='none', max_length=4000)),
                ('linkedin_url', models.URLField(default='https://example.com', max_length=500)),
                ('instagram_url', models.URLField(default='https://example.com', max_length=500)),
                ('facebook', models.URLField(default='https://example.com', max_length=500)),
                ('webiste', models.URLField(default='https://example.com', max_length=500)),
                ('Key_highlights', models.CharField(default='highlights', max_length=2000)),
                ('cover_image', models.ImageField(default='cover_image', upload_to='company_images/')),
                ('other_image1', models.ImageField(default='img1', upload_to='company_images/')),
                ('other_image2', models.ImageField(default='img2', upload_to='company_images/')),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
