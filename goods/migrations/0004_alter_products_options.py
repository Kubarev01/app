# Generated by Django 4.2.11 on 2024-05-28 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ('id',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
