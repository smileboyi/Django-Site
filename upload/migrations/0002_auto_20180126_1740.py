# Generated by Django 2.0.1 on 2018-01-26 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='用户名')),
                ('headImg', models.FileField(upload_to='./upload', verbose_name='文件')),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]