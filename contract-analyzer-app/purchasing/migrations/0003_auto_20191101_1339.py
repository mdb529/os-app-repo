# Generated by Django 2.2.5 on 2019-11-01 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0002_auto_20191031_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'get_latest_by': ['-invoice_date'], 'verbose_name': 'Purchase', 'verbose_name_plural': 'Purchases'},
        ),
    ]
