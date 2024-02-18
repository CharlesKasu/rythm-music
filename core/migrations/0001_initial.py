# Generated by Django 3.1.14 on 2024-01-08 20:36

import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('thumbnail', models.ImageField(default='artists/default.png', upload_to='artists')),
                ('bio', models.TextField(null=True, verbose_name='Artist Bio')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('thumbnail', models.ImageField(default='genres/default.png', upload_to='genres')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_id', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=200, verbose_name='Song name')),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='thumbnails')),
                ('song', models.FileField(max_length=500, upload_to=core.models.song_directory_path)),
                ('size', models.IntegerField(default=0)),
                ('playtime', models.CharField(default='0.00', max_length=10)),
                ('type', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('artists', models.ManyToManyField(related_name='songs', to='core.Artist')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
