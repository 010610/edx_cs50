# Generated by Django 2.2.5 on 2019-10-12 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20191012_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addition',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
