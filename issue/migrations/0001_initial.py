# Generated by Django 3.0.3 on 2020-04-30 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_auto_20200430_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.IntegerField(choices=[(0, 'Issue'), (1, 'Article')])),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField()),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
                ('liker', models.ManyToManyField(related_name='issue_liker', to='account.User')),
            ],
        ),
        migrations.CreateModel(
            name='IssueCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField()),
                ('content', models.TextField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issue.Issue')),
                ('liker', models.ManyToManyField(related_name='answer_liker', to='account.User')),
                ('replier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
        ),
    ]