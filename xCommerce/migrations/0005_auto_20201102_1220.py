# Generated by Django 3.1.2 on 2020-11-02 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xCommerce', '0004_auto_20201102_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xCommerce.product'),
        ),
    ]