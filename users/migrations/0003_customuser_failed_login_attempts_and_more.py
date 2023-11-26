# Generated by Django 4.2.7 on 2023-11-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_studentgroup_subject_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='failed_login_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lockout_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
