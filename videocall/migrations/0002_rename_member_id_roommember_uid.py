# Generated by Django 4.0.1 on 2022-01-06 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videocall', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roommember',
            old_name='member_id',
            new_name='uid',
        ),
    ]
