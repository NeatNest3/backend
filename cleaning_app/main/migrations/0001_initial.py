# Generated by Django 5.1.2 on 2024-12-05 01:44

import cleaning_app.main.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('s3_url', models.URLField(blank=True, max_length=500, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('phone', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_of_birth', models.DateField()),
                ('allergies', models.JSONField(blank=True, default=cleaning_app.main.models.User.default_allergies, null=True)),
                ('role', models.CharField(choices=[('customer', 'Customer'), ('cleaner', 'Cleaner')], default='customer', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('bio', models.TextField(blank=True, max_length=750)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('address_line_one', models.CharField(max_length=255)),
                ('address_line_two', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('home_type', models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('townhouse', 'Townhouse'), ('other', 'Other')], max_length=50)),
                ('bedrooms', models.CharField(blank=True, max_length=2, null=True)),
                ('bathrooms', models.FloatField(blank=True, max_length=3, null=True)),
                ('pets', models.JSONField(default=dict)),
                ('kids', models.CharField(max_length=2)),
                ('special_instructions', models.TextField(blank=True, max_length=1000, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homes', to='main.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('booked', 'Booked'), ('active', 'Active'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='main.customer')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='main.home')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_role', models.CharField(max_length=10)),
                ('reviewee_role', models.CharField(max_length=10)),
                ('review_text', models.TextField()),
                ('review_date', models.DateField()),
                ('rating', models.FloatField(verbose_name=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.job')),
                ('reviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='main.home')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='rooms',
            field=models.ManyToManyField(related_name='jobs', to='main.room'),
        ),
        migrations.CreateModel(
            name='Service_Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flexible_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('pet_friendly', models.BooleanField(default=True)),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('preferred_rooms', models.JSONField(default=cleaning_app.main.models.Service_Provider.default_rooms)),
                ('background_check', models.BooleanField(default=False)),
                ('bio_work_history', models.TextField(blank=True, max_length=1000)),
                ('country', models.CharField(max_length=50)),
                ('address_line_one', models.CharField(max_length=255)),
                ('address_line_two', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('specialties', models.ManyToManyField(blank=True, related_name='service_providers', to='main.specialty')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='service_provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs', to='main.service_provider'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('duration', models.DurationField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('service_provider_notes', models.TextField(blank=True, null=True)),
                ('customer_notes', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_jobs', to='main.job')),
                ('room', models.ForeignKey(default='General', on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='main.room')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='tasks',
            field=models.ManyToManyField(related_name='job_tasks', to='main.task'),
        ),
    ]
