# Generated by Django 4.1.3 on 2022-12-03 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_date_ordred_orederitem_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orederitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]