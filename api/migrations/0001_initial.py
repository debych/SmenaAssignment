# Generated by Django 3.1.5 on 2021-01-11 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name="Printer's name")),
                ('api_key', models.CharField(max_length=64, verbose_name="Printer's API key")),
                ('check_type', models.CharField(choices=[('kitchen', 'for kitchen'), ('client', 'for client')], max_length=32, verbose_name='Type of printed checks')),
                ('point_id', models.IntegerField(verbose_name="ID of the printer's point")),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('kitchen', 'for kitchen'), ('client', 'for client')], max_length=32, verbose_name='Check type')),
                ('order', models.JSONField(verbose_name='Order')),
                ('status', models.CharField(choices=[('new', 'new'), ('rendered', 'rendered'), ('printed', 'printed')], default='new', max_length=32, verbose_name='Check status')),
                ('pdf_file', models.FileField(upload_to='')),
                ('printer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.printer', verbose_name='Printer that check belongs to')),
            ],
        ),
    ]
