# Generated by Django 3.0.6 on 2020-11-18 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201117_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='kakao_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_hide',
            field=models.BooleanField(default=False),
        ),
    ]
