from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0009_job_company'),  # Add the correct previous migration dependency
        # ...existing dependencies...
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(
                max_length=10,
                choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time')],
                default='full_time',
            ),
        ),
    ]
