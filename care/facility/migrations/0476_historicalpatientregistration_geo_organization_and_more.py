# Generated by Django 5.1.3 on 2024-12-23 19:12

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0034_organization_level_cache'),
        ('facility', '0475_merge_20241223_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatientregistration',
            name='geo_organization',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='emr.organization'),
        ),
        migrations.AddField(
            model_name='historicalpatientregistration',
            name='organization_cache',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
        migrations.AddField(
            model_name='patientregistration',
            name='geo_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='emr.organization'),
        ),
        migrations.AddField(
            model_name='patientregistration',
            name='organization_cache',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]