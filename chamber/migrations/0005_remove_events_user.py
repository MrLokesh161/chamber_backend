# Generated by Django 5.0.3 on 2024-03-17 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chamber', '0004_events_linkforevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='user',
        ),
    ]
