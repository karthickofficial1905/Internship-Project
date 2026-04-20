# Generated migration for adding review_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio_details', '0023_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='review_type',
            field=models.CharField(
                choices=[('normal', 'Normal Review'), ('technical', 'Technical Review')],
                default='normal',
                max_length=20
            ),
        ),
    ]