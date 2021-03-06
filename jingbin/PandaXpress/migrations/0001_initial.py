# Generated by Django 3.1.7 on 2021-04-22 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Follow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Has',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrient_amnt', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Has',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('ingredient_id', models.AutoField(primary_key=True, serialize=False)),
                ('ingredient_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Ingredients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('inventory_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Inventory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryIncl',
            fields=[
                ('inventory_incl_id', models.AutoField(primary_key=True, serialize=False)),
                ('inventory_id', models.IntegerField()),
                ('ingredient_id', models.IntegerField()),
                ('ingredient_amount', models.FloatField()),
                ('ingredient_unit', models.CharField(max_length=50)),
                ('ingredient_added_date', models.DateField()),
                ('ingredient_expiry_date', models.DateField()),
            ],
            options={
                'db_table': 'Inventory_incl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('pwd', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Membership',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nutrients',
            fields=[
                ('nutrient_id', models.IntegerField(primary_key=True, serialize=False)),
                ('nutrient_name', models.CharField(blank=True, max_length=25, null=True)),
                ('nutrient_description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'Nutrients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Owns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Owns',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('recipe_id', models.AutoField(primary_key=True, serialize=False)),
                ('recipe_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('recipe_genre', models.CharField(blank=True, max_length=1000, null=True)),
                ('recipe_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('recipe_steps', models.TextField(blank=True, null=True)),
                ('cooking_time', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Recipes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_member_rel', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'Store',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeIncl',
            fields=[
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='PandaXpress.recipes')),
            ],
            options={
                'db_table': 'Recipe_Incl',
                'managed': False,
            },
        ),
    ]
