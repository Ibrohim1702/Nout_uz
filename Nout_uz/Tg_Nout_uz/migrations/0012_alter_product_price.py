# Generated by Django 4.1 on 2022-08-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tg_Nout_uz', '0011_remove_product_brendi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]
