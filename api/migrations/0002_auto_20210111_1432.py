# Generated by Django 3.1.5 on 2021-01-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='pdf_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
