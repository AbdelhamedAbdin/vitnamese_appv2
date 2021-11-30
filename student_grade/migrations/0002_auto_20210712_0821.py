# Generated by Django 3.1.2 on 2021-07-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_grade', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='character_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='complexity_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='complexity_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='regularity_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='regularity_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_class_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_class_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_type_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_type_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_number_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_number_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_unit_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='error_unit_zh_hans',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
