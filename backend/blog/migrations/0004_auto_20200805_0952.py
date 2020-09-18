# Generated by Django 2.2.14 on 2020-08-05 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_usergroup_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='name',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='eng_name',
            field=models.CharField(default='Awefawef', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergroup',
            name='kor_name',
            field=models.CharField(default='asdfadf', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='department',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='pin',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='position',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
