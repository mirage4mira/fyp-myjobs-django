from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0006_employer_user'),  # Added missing dependency
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('salary', models.DecimalField(max_digits=10, decimal_places=2)),
                ('number_of_candidates', models.PositiveIntegerField()),
                ('required_education', models.CharField(max_length=255)),
                ('required_experience_years', models.PositiveIntegerField()),
            ],
        ),
    ]
