# Generated by Django 2.0 on 2018-03-27 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winners', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='country',
            name='alpha_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='lat',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='lng',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='numeric_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
