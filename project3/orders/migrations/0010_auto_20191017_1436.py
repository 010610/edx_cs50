# Generated by Django 2.2.5 on 2019-10-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20191016_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='n_addition',
        ),
        migrations.RemoveField(
            model_name='item',
            name='addition',
        ),
        migrations.AddField(
            model_name='item',
            name='addition',
            field=models.ManyToManyField(related_name='additions', to='orders.Addition'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='item',
            name='topping',
        ),
        migrations.AddField(
            model_name='item',
            name='topping',
            field=models.ManyToManyField(related_name='toppings', to='orders.Topping'),
        ),
    ]
