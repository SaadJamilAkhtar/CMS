# Generated by Django 3.2.8 on 2021-11-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='Group',
            field=models.ManyToManyField(blank=True, null=True, to='main.Group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]