# Generated by Django 4.2.7 on 2023-11-26 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_alter_mainbooks_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.ImageField(default='languages/bg2.png', null=True, upload_to='languages/'),
        ),
    ]
