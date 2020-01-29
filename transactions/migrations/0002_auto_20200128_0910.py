# Generated by Django 3.0.2 on 2020-01-28 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('food', 'food'), ('bills', 'bills'), ('car', 'car'), ('transport', 'transport'), ('income', 'income'), ('transfer', 'transfer')], max_length=50),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
