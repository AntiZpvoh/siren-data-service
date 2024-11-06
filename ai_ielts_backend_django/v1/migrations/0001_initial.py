# Generated by Django 4.2.16 on 2024-11-06 07:07

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='user id')),
                ('username', models.CharField(max_length=200, unique=True, verbose_name='user name')),
                ('token', models.CharField(max_length=100, verbose_name='user token')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='user created time')),
                ('modifiedTime', models.DateTimeField(auto_now=True, verbose_name='user modified time')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
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
            name='QuestionGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='question group id')),
                ('name', models.CharField(max_length=100, verbose_name='question group name')),
                ('type', models.CharField(choices=[('1', 'Part 1'), ('2&3', 'Part 2 & 3')], max_length=10, verbose_name='question group type (1 or 2&3)')),
                ('topic', models.CharField(max_length=200, verbose_name='question group topic')),
                ('description', models.TextField(verbose_name='question group description')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='question group created time')),
                ('modifiedTime', models.DateTimeField(auto_now=True, verbose_name='question group modified time')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='session id')),
                ('openaiSessionId', models.CharField(max_length=100, verbose_name='openai session id')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='session created time')),
                ('modifiedTime', models.DateTimeField(auto_now=True, verbose_name='session modified time')),
                ('questionGroups', models.ManyToManyField(to='v1.questiongroup', verbose_name='question groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user id related to session')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='question id')),
                ('partType', models.BigIntegerField(choices=[(1, 'Part 1'), (2, 'Part 2'), (3, 'Part 3')], verbose_name='part type (1 or 2 or 3)')),
                ('content', models.TextField(verbose_name='question content')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='question created time')),
                ('modifiedTime', models.DateTimeField(auto_now=True, verbose_name='question modified time')),
                ('questionGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.questiongroup', verbose_name='question group id for question')),
            ],
        ),
        migrations.CreateModel(
            name='LearningProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isCompleted', models.BooleanField(verbose_name='Has this question group already learnt?')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='learning progress created time')),
                ('modifiedTime', models.DateTimeField(auto_now=True, verbose_name='learning progress modified time')),
                ('questionGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v1.questiongroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='questionGroupLearningProgress',
            field=models.ManyToManyField(through='v1.LearningProgress', to='v1.questiongroup', verbose_name='user learning progress for some question group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]