# Generated by Django 5.1.2 on 2024-10-12 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_description_alter_product_promotions_and_more'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ('collection1')
        """, """
            DELETE FROM store_collection
            WHERE title = 'collection1'
        """)
    ]
