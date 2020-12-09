# Generated by Django 3.0.6 on 2020-12-03 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_product_cs_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='CS_contact',
            field=models.CharField(max_length=500, verbose_name='1대1 상담 url'),
        ),
        migrations.AlterField(
            model_name='product',
            name='free_shipping',
            field=models.BooleanField(default=False, verbose_name='택배거래'),
        ),
        migrations.AlterField(
            model_name='product',
            name='same_day_shipping',
            field=models.BooleanField(default=False, verbose_name='직거래'),
        ),
    ]