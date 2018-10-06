# Generated by Django 2.1.1 on 2018-10-06 05:55

from django.db import migrations
import oauth.models
import project.validators
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_auto_20181006_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to=oauth.models.get_logo_path, validators=[project.validators.MinImageDimensionsValidator(512, 512), project.validators.MaxImageDimensionsValidator(1024, 1024), project.validators.SquareImageValidator()], verbose_name="App's logo"),
        ),
    ]
