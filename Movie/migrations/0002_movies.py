# Generated by Django 3.1.4 on 2020-12-08 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='movieimg/')),
                ('release_year', models.CharField(max_length=4)),
                ('Genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movie.genre')),
            ],
        ),
    ]
