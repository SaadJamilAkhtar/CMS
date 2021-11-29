# Generated by Django 3.2.8 on 2021-11-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_connecteddata_extrafields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connecteddata',
            name='client',
        ),
        migrations.AddField(
            model_name='connecteddata',
            name='client',
            field=models.ManyToManyField(to='main.Client'),
        ),
        migrations.RemoveField(
            model_name='connecteddata',
            name='field',
        ),
        migrations.AddField(
            model_name='connecteddata',
            name='field',
            field=models.ManyToManyField(blank=True, null=True, to='main.ExtraFields'),
        ),
    ]