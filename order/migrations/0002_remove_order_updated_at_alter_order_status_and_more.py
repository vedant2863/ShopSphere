# Generated by Django 5.1.4 on 2025-01-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.CharField(max_length=255),
        ),
    ]
