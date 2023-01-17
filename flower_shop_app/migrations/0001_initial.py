# Generated by Django 4.1.5 on 2023-01-17 22:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('availability', models.BooleanField(default=False, verbose_name='наличие')),
                ('quantity', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='количество')),
            ],
            options={
                'verbose_name': 'цветок',
                'verbose_name_plural': 'цветы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FlowerBouquet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='букет')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='картинка')),
                ('availability', models.BooleanField(default=False, verbose_name='наличие')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлен')),
            ],
            options={
                'verbose_name': 'букет',
                'verbose_name_plural': 'букеты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FlowerBouquetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flower_quantity', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество цветов в букете')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, verbose_name='имя клиента')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='номер телефона')),
                ('address', models.CharField(max_length=250, verbose_name='адрес')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата и время заказа')),
                ('delivery_time', models.SmallIntegerField(choices=[(10, 'C 10:00 до 12:00'), (12, 'C 12:00 до 14:00'), (14, 'C 14:00 до 16:00'), (16, 'C 16:00 до 18:00'), (18, 'C 18:00 до 20:00')], verbose_name='время доставки')),
                ('status', models.SmallIntegerField(choices=[(1, 'Обрабатывается'), (2, 'Собирается'), (3, 'В доставке'), (4, 'Выполнен')], default=1, verbose_name='статус заказа')),
            ],
            options={
                'verbose_name': 'букет',
                'verbose_name_plural': 'букеты',
                'ordering': ['status', '-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество')),
                ('flower_bouquet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='flower_shop_app.flowerbouquet', verbose_name='букет')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='flower_shop_app.order', verbose_name='заказ')),
            ],
            options={
                'verbose_name': 'букет',
                'verbose_name_plural': 'букеты',
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status', '-created'], name='flower_shop_status_e649ad_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phone_number'], name='flower_shop_phone_n_21a4ef_idx'),
        ),
        migrations.AddField(
            model_name='flowerbouquetitem',
            name='flower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flower_bouquet_items', to='flower_shop_app.flower', verbose_name='цветок'),
        ),
        migrations.AddField(
            model_name='flowerbouquetitem',
            name='flower_bouquet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flower_bouquet_items', to='flower_shop_app.flowerbouquet', verbose_name='букет'),
        ),
        migrations.AddField(
            model_name='flowerbouquet',
            name='flowers',
            field=models.ManyToManyField(related_name='flower_bouquets', through='flower_shop_app.FlowerBouquetItem', to='flower_shop_app.flower', verbose_name='цветы'),
        ),
        migrations.AddIndex(
            model_name='flower',
            index=models.Index(fields=['availability'], name='flower_shop_availab_5d1878_idx'),
        ),
        migrations.AddIndex(
            model_name='flower',
            index=models.Index(fields=['name'], name='flower_shop_name_683bb5_idx'),
        ),
        migrations.AddIndex(
            model_name='flowerbouquet',
            index=models.Index(fields=['price'], name='flower_shop_price_475a3d_idx'),
        ),
        migrations.AddIndex(
            model_name='flowerbouquet',
            index=models.Index(fields=['name'], name='flower_shop_name_6af213_idx'),
        ),
        migrations.AddIndex(
            model_name='flowerbouquet',
            index=models.Index(fields=['availability'], name='flower_shop_availab_7fa00d_idx'),
        ),
    ]
