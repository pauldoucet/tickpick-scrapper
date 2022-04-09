# Generated by Django 4.0.3 on 2022-04-06 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=200)),
                ('venue_id', models.CharField(max_length=200)),
                ('date_event', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
    ]