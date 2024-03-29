# Generated by Django 5.0.1 on 2024-01-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='apartment',
            new_name='api_apartme_area_2a50a4_idx',
            old_fields=('area', 'rooms_no', 'price_month', 'price_month', 'currency'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='currency',
            field=models.CharField(choices=[('EUR', 'EUR'), ('USD', 'USD')], db_index=True, default='EUR', max_length=3),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
