# Generated by Django 3.1.2 on 2020-11-02 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xCommerce', '0003_auto_20201102_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
