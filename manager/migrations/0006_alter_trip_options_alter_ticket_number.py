# Generated by Django 4.1.7 on 2023-03-30 11:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0005_ticket_price_alter_ticket_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="trip",
            options={"ordering": ["id"]},
        ),
        migrations.AlterField(
            model_name="ticket",
            name="number",
            field=models.AutoField(default=18633, primary_key=True, serialize=False),
        ),
    ]
