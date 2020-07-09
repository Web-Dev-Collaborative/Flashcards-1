# Generated by Django 3.0.8 on 2020-07-09 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150, verbose_name='Box description')),
                ('position', models.IntegerField(verbose_name='Position of the box in the session')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front_text', models.CharField(max_length=150, verbose_name='Front text')),
                ('back_text', models.TextField(verbose_name='Back text')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last modified on')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150, verbose_name='Session description')),
                ('stage', models.IntegerField(default=0)),
                ('is_running', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CardBoxRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_position_in_box', models.IntegerField(verbose_name='Position number of the card in the box')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leitner.Box')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leitner.Card')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='boxes',
            field=models.ManyToManyField(through='leitner.CardBoxRelation', to='leitner.Box'),
        ),
        migrations.AddField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='box',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leitner.Session'),
        ),
    ]
