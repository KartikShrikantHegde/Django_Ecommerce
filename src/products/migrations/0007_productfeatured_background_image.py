# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productfeatured'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatured',
            name='background_image',
            field=models.BooleanField(default=False),
        ),
    ]
