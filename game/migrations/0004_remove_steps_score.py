# Generated by Django 3.0.7 on 2020-06-10 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20200609_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steps',
            name='score',
        ),
    ]