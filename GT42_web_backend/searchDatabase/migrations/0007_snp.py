# Generated by Django 5.0.3 on 2024-04-03 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchDatabase', '0006_alter_haplotype_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='snp',
            fields=[
                ('mosaicID', models.CharField(max_length=255)),
                ('SNPSite', models.IntegerField()),
                ('SNPType', models.CharField(max_length=255)),
                ('IsoSeqEvidence', models.CharField(max_length=255)),
                ('RNASeqEvidence', models.CharField(max_length=255)),
                ('haplotypeSNP', models.TextField()),
                ('color', models.CharField(max_length=255)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'snp',
                'managed': False,
            },
        ),
    ]
