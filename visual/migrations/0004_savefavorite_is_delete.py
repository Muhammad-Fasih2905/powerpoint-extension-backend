# Generated by Django 4.1.5 on 2024-01-27 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual', '0003_flowchart_created_flowchart_updated_graph_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='savefavorite',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
