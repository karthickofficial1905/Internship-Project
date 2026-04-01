# Custom migration to add missing name column to currency table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0002_alter_brand_id_alter_cart_id_alter_cartitem_id_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE currency ADD COLUMN name VARCHAR(50) DEFAULT '';",
            reverse_sql="ALTER TABLE currency DROP COLUMN name;"
        ),
    ]