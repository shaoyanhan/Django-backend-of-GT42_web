# Generated by Django 5.0.3 on 2024-04-23 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchDatabase', '0011_alter_gt42genomeid_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='GT42NextID',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nextID', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'gt42_next_id',
                'managed': False,
            },
        ),
    ]
