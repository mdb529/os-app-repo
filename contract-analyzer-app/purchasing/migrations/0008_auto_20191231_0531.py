# Generated by Django 2.2.6 on 2019-12-31 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0007_auto_20191120_0424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='drug_name',
        ),
        migrations.AddField(
            model_name='purchase',
            name='drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='purchasing.Drug'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='ndc_code',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
    ]
