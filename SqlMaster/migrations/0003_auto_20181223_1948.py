# Generated by Django 2.1.4 on 2018-12-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SqlMaster', '0002_auto_20181222_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opeiation',
            name='code',
            field=models.PositiveSmallIntegerField(verbose_name='操作码'),
        ),
        migrations.AlterField(
            model_name='users',
            name='age',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=14, null=True, unique=True, verbose_name='手机号'),
        ),
    ]
