# Generated by Django 3.0.4 on 2020-05-04 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('account', '0004_auto_20200430_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField()),
                ('content', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='account.User')),
                ('likers', models.ManyToManyField(related_name='comment_liker', to='account.User')),
                ('parent_comment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='comment.Comment')),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='account.User')),
            ],
        ),
    ]
