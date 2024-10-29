from django.db import migrations, models

def create_default_config(apps, schema_editor):
    Configuration = apps.get_model('configuration', 'Configuration')
    Configuration.objects.create(key='COLAB_API_URL', value='')


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('value', models.TextField()),
            ],
        ),
        migrations.RunPython(create_default_config),
    ]
