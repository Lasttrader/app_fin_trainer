# Generated by Django 4.1.4 on 2023-06-08 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_board', '0005_remove_post_postcategory_delete_postcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upload',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
