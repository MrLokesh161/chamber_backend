# Generated by Django 5.0.3 on 2024-03-17 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamber', '0003_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='LinkforEvent',
            field=models.URLField(null=True),
        ),
    ]
