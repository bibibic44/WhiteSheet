# Generated by Django 3.2.3 on 2021-05-27 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_alter_review_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]