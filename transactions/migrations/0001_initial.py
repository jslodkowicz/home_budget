# Generated by Django 3.0.2 on 2020-01-27 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default', max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('exp', 'expense'), ('inc', 'income')], max_length=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=models.SET(None), to='transactions.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='transactions.Wallet')),
            ],
        ),
    ]
