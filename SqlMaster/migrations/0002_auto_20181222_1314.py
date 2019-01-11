# Generated by Django 2.1.4 on 2018-12-22 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SqlMaster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opeiation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='操作码')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='auth',
            field=models.BooleanField(default=False, verbose_name='是否为root用户'),
        ),
        migrations.AlterField(
            model_name='login',
            name='name',
            field=models.ForeignKey(on_delete='CASCADE', to='SqlMaster.Users', verbose_name='登陆用户'),
        ),
        migrations.AddField(
            model_name='opeiation',
            name='user',
            field=models.ForeignKey(on_delete='CASCADE', to='SqlMaster.Users', verbose_name='操作用户'),
        ),
    ]
