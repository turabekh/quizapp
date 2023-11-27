# Generated by Django 4.2.7 on 2023-11-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_remove_course_assessment_criteria_assessmentcriteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentcriteria',
            name='criteria_type',
            field=models.CharField(choices=[('pass', 'Pass'), ('merit', 'Merit'), ('distinction', 'Distinction')], default='pass', max_length=20),
        ),
    ]