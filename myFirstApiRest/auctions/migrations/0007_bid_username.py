# Generated by Django 5.1.7 on 2025-04-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_auction_auctioneer"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="username",
            field=models.CharField(default="PSmith", max_length=150),
            preserve_default=False,
        ),
    ]
