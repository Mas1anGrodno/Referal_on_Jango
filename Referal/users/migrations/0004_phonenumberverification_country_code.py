# Generated by Django 5.1.3 on 2024-12-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_phonenumberverification_activated_referal_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumberverification',
            name='country_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
