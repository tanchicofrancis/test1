# Generated by Django 5.1.2 on 2025-01-19 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_orderitem_ram'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='rom',
            field=models.CharField(choices=[('256GB', '256GB'), ('512GB', '512GB'), ('1TB', '1TB')], default='256GB', max_length=5),
        ),
    ]
