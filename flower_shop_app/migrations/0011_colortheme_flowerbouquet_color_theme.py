# Generated by Django 4.1.5 on 2023-01-23 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flower_shop_app', '0010_alter_order_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
            ],
            options={
                'verbose_name': 'основной цвет букета',
                'verbose_name_plural': 'основные цвета букета',
            },
        ),
        migrations.AddField(
            model_name='flowerbouquet',
            name='color_theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flower_bouquets', to='flower_shop_app.colortheme'),
        ),
    ]
