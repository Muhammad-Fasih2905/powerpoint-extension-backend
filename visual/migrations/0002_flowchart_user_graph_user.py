# Generated by Django 4.1.5 on 2024-01-05 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visual', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowchart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_flowchart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='graph',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_graph', to=settings.AUTH_USER_MODEL),
        ),
    ]
