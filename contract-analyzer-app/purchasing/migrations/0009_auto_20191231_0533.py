# Generated by Django 2.2.6 on 2019-12-31 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0008_auto_20191231_0531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='drug',
            new_name='drug_name',
        ),
    ]
