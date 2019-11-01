# Generated by Django 2.2.5 on 2019-10-12 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191012_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('S', 'Small'), ('L', 'Large'), ('R', 'Regular')], default='R', max_length=1),
        ),
    ]
