# Generated by Django 3.2.9 on 2021-11-30 05:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientToDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('clients', models.ManyToManyField(through='accounts.ClientToDepartment', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='accounts.department')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='LegalEntity',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('full_name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('short_name', models.CharField(max_length=500, verbose_name='Short name')),
                ('inn', models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1000000000)], verbose_name='INN')),
                ('kpp', models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(999999999), django.core.validators.MinValueValidator(100000000)], verbose_name='KPP')),
                ('departments', mptt.fields.TreeManyToManyField(to='accounts.Department')),
            ],
            options={
                'verbose_name': 'Legal entity',
                'verbose_name_plural': 'Legal entities',
            },
        ),
        migrations.AddField(
            model_name='clienttodepartment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
        ),
    ]
