# Generated by Django 4.1.7 on 2023-05-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0003_tx_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='miner_address',
            field=models.CharField(default='0x0', editable=False, max_length=64),
        ),
        migrations.AddField(
            model_name='block',
            name='total_fee',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='block',
            name='hash',
            field=models.CharField(default='0x0', editable=False, max_length=64),
        ),
        migrations.AlterField(
            model_name='block',
            name='previous_hash',
            field=models.CharField(default='GENESIS BLOCK', editable=False, max_length=64),
        ),
    ]