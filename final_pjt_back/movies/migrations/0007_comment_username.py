# Generated by Django 3.2.3 on 2021-05-26 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
