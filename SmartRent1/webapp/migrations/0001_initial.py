# Generated by Django 2.0.5 on 2018-05-17 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('agent_img', models.URLField(null=True)),
                ('company', models.CharField(blank=True, max_length=20, null=True)),
                ('company_logo', models.URLField(null=True)),
                ('fri_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('res_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('bond_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('comment', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('house_img', models.URLField(null=True)),
                ('loc_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('fac_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('tran_rating', models.DecimalField(decimal_places=1, max_digits=5)),
                ('comment', models.CharField(blank=True, max_length=20)),
                ('no_bed', models.IntegerField(blank=True, null=True)),
                ('no_bath', models.IntegerField(blank=True, null=True)),
                ('house_type', models.CharField(blank=True, max_length=20)),
                ('distance_umel', models.IntegerField(blank=True)),
                ('distance_rmit', models.IntegerField(blank=True)),
                ('duration_umel', models.IntegerField(blank=True)),
                ('duration_rmit', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Agency')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Property')),
            ],
        ),
    ]
