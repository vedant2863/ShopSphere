# Generated by Django 5.1.4 on 2025-01-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
