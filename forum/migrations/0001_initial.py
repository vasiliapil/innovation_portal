# Generated by Django 4.2.11 on 2024-05-22 06:04

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
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Τίτλος', models.CharField(max_length=50)),
                ('Περιγραφή', models.CharField(max_length=100)),
                ('Συγγραφέας', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Δημοσίευση', models.DateTimeField(default=django.utils.timezone.now)),
                ('Τίτλος', models.CharField(default='untitled', max_length=50)),
                ('Περιεχόμενο', models.TextField()),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.topic')),
                ('Συγγραφέας', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Δημοσίευση', models.DateTimeField(default=django.utils.timezone.now)),
                ('Περιεχόμενο', models.TextField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.post')),
                ('Συγγραφέας', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
