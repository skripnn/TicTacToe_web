# Generated by Django 3.0.7 on 2020-06-10 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_score'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='field',
            new_name='field_str',
        ),
    ]
