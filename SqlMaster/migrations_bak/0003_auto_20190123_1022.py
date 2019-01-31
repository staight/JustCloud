# Generated by Django 2.1.5 on 2019-01-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SqlMaster', '0002_auto_20190122_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='system',
            old_name='creatuser',
            new_name='createuser',
        ),
        migrations.AddField(
            model_name='system',
            name='devicecode',
            field=models.CharField(max_length=20, null=True, verbose_name='设备注册码'),
        ),
        migrations.AddField(
            model_name='system',
            name='key',
            field=models.CharField(max_length=26, null=True, verbose_name='API密钥'),
        ),
        migrations.AddField(
            model_name='system',
            name='protocol',
            field=models.CharField(default='COAP', max_length=4, verbose_name='接入协议'),
        ),
    ]