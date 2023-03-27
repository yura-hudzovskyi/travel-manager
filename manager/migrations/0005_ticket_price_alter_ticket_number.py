# Generated by Django 4.1.7 on 2023-03-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0004_remove_ticket_id_alter_ticket_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=6, null=True
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="number",
            field=models.AutoField(default=12666, primary_key=True, serialize=False),
        ),
    ]