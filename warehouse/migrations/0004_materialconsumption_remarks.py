# Generated by Django 5.1.4 on 2025-01-21 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_issuematerial_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialconsumption',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
