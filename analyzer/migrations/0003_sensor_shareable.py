# Generated by Django 2.0.5 on 2018-05-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0002_dataitem_previous_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='shareable',
            field=models.BooleanField(default=False),
        ),
    ]
