# Generated by Django 3.1.5 on 2021-01-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210114_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
