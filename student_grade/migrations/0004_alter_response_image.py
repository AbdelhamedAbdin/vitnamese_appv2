# Generated by Django 3.2.6 on 2021-08-26 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_grade', '0003_auto_20210712_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
