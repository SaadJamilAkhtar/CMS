# Generated by Django 3.2.6 on 2021-12-22 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20211209_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportDataFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='assets/uploads/')),
            ],
        ),
    ]