# Generated by Django 4.1.4 on 2023-04-02 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0009_category_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='postCategory_en_us',
            field=models.ManyToManyField(null=True, through='NewsPortal.PostCategory', to='NewsPortal.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='postCategory_ru',
            field=models.ManyToManyField(null=True, through='NewsPortal.PostCategory', to='NewsPortal.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='postText_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='postText_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='postTitle_en_us',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='postTitle_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='PostCategory_ru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryThrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.category')),
                ('postThrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.post')),
            ],
            options={
                'verbose_name': 'post category [ru]',
                'verbose_name_plural': 'post categorys [ru]',
                'db_table': 'NewsPortal_postcategory_ru',
                'db_tablespace': '',
                'auto_created': False,
            },
        ),
        migrations.CreateModel(
            name='PostCategory_en_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryThrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.category')),
                ('postThrough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.post')),
            ],
            options={
                'verbose_name': 'post category [en-us]',
                'verbose_name_plural': 'post categorys [en-us]',
                'db_table': 'NewsPortal_postcategory_en_us',
                'db_tablespace': '',
                'auto_created': False,
            },
        ),
    ]
