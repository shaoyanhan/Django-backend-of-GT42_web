# Generated by Django 5.0.3 on 2024-04-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchDatabase', '0008_transcript'),
    ]

    operations = [
        migrations.CreateModel(
            name='GT42GenomeID',
            fields=[
                ('genomeID', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'gt42genomeid',
                'managed': False,
            },
        ),
    ]
