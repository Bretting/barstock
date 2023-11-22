# Generated by Django 4.2.3 on 2023-11-22 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_compare', '0002_tracked_products_start_price_change_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracked_products',
            name='previous_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
    ]