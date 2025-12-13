from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("torque", "0048_rename_search_cache_dirty_wikiconfig_cache_dirty"),
    ]

    operations = [
        migrations.RenameModel('CsvSpecification', 'SpreadsheetSpecification')
    ]
