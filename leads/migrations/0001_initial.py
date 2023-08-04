# Generated by Django 4.1.6 on 2023-08-04 09:03

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import leads.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_organizer', models.BooleanField(default=True)),
                ('is_agent', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
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
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New', max_length=30)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LeadSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lookup_Names',
            fields=[
                ('lookup_names_id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=240, null=True)),
                ('created_by', models.IntegerField(default=-1, null=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('app_id', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreferredContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RepeatOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('referenceNotes', models.CharField(blank=True, max_length=500, null=True)),
                ('reminder', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatusOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAttendees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.userprofile')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='designated_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designatedLead', to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='task',
            name='invitees',
            field=models.ManyToManyField(blank=True, to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization', to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='task',
            name='repeat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.repeatoptions'),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.taskstatusoptions'),
        ),
        migrations.CreateModel(
            name='Parties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('primary_number', models.CharField(max_length=30)),
                ('whatsapp_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now)),
                ('tenant_map_id', models.IntegerField(default=1)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.agent')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.userprofile')),
                ('preferred_contact_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.preferredcontact')),
                ('user_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='Lookup_Name_Values',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, null=True)),
                ('meaning', models.CharField(max_length=240, null=True)),
                ('description', models.CharField(blank=True, max_length=240, null=True)),
                ('tag', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('enabled_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(default=-1, null=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('lookup_names_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.lookup_names')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now)),
                ('converted_date', models.DateTimeField(blank=True, null=True)),
                ('tenant_map_id', models.IntegerField(default=1)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.agent')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.userprofile')),
                ('party', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.parties')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.leadsource')),
                ('status', models.ForeignKey(default='New', null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.category')),
            ],
        ),
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=leads.models.handle_upload_follow_ups)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='followups', to='leads.lead')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='agent',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
