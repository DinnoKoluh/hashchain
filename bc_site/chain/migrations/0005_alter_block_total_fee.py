# Generated by Django 4.1.7 on 2023-05-02 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0004_block_miner_address_block_total_fee_alter_block_hash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='total_fee',
            field=models.FloatField(default=0, editable=False),
        ),
    ]
