# Generated by Django 5.1.2 on 2025-01-19 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_orderitem_ram_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='ram',
            field=models.CharField(choices=[('12GB', '12GB'), ('16GB', '16GB')], default='12GB', max_length=4),
        ),
    ]
