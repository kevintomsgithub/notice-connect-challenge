# Generated by Django 3.2.3 on 2021-05-17 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_match_match_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_type',
            field=models.CharField(choices=[('1', 'Strong Match'), ('2', 'Possible Match'), ('3', 'Weak Match')], max_length=100),
        ),
    ]