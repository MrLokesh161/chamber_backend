# Generated by Django 5.0.3 on 2024-03-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamber', '0005_remove_events_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Email', models.EmailField(max_length=254)),
                ('phonenumber', models.BigIntegerField()),
                ('Description', models.CharField(max_length=1000)),
            ],
        ),
    ]
