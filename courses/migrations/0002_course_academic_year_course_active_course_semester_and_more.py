# Generated by Django 4.2.7 on 2023-11-25 02:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='academic_year',
            field=models.CharField(choices=[('2023-2024', '2023-2024'), ('2024-2025', '2024-2025'), ('2025-2026', '2025-2026'), ('2026-2027', '2026-2027'), ('2027-2028', '2027-2028'), ('2028-2029', '2028-2029'), ('2029-2030', '2029-2030'), ('2030-2031', '2030-2031'), ('2031-2032', '2031-2032')], default='2023-2024', max_length=9),
        ),
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('first', 'First Semester'), ('second', 'Second Semester'), ('summer', 'Summer')], default='first', max_length=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='taught_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
