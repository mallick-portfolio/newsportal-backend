# Generated by Django 5.0.1 on 2024-01-18 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_newattachment_alter_news_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewAttachment',
            new_name='PostAttachment',
        ),
    ]