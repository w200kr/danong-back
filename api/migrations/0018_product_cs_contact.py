# Generated by Django 3.0.6 on 2020-12-02 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20201130_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='CS_contact',
            field=models.CharField(default='', max_length=100, verbose_name='1대1 상담 url'),
            preserve_default=False,
        ),
    ]