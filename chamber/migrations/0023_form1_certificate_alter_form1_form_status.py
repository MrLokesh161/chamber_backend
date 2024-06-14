# Generated by Django 5.0.3 on 2024-05-21 06:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamber', '0022_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='form1',
            name='certificate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form1_certificates', to='chamber.certificate'),
        ),
        migrations.AlterField(
            model_name='form1',
            name='form_status',
            field=models.CharField(choices=[('pending', 'pending'), ('Approved by AO', 'Approved by AO'), ('Approved by CEO', 'Approved by CEO'), ('Approved by Membership Committee', 'Approved by Membership Committee'), ('Approved by OB', 'Approved by OB'), ('Approved as a Member', 'Approved as a Member'), ('waiting for payment', 'waiting for payment'), ('payment done (approved as Member)', ''), ('rejected', 'rejected')], default='pending', max_length=50),
        ),
    ]
