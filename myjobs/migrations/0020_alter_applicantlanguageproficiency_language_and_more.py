# Generated by Django 5.1.7 on 2025-04-10 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjobs', '0019_rename_date_created_job_date_created_or_renewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantlanguageproficiency',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Mandarin', 'Mandarin'), ('Malay', 'Malay'), ('Tamil', 'Tamil'), ('Spanish', 'Spanish'), ('French', 'French'), ('German', 'German'), ('Japanese', 'Japanese'), ('Korean', 'Korean'), ('Arabic', 'Arabic')], max_length=100),
        ),
        migrations.AlterField(
            model_name='applicantskill',
            name='name',
            field=models.CharField(choices=[('Programming', 'Programming'), ('Data Analysis', 'Data Analysis'), ('Project Management', 'Project Management'), ('Graphic Design', 'Graphic Design'), ('Digital Marketing', 'Digital Marketing'), ('Sales', 'Sales'), ('Customer Service', 'Customer Service'), ('Content Writing', 'Content Writing'), ('Public Speaking', 'Public Speaking'), ('Problem Solving', 'Problem Solving')], max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(choices=[('Kuala Lumpur', 'Kuala Lumpur'), ('George Town', 'George Town'), ('Ipoh', 'Ipoh'), ('Shah Alam', 'Shah Alam'), ('Petaling Jaya', 'Petaling Jaya'), ('Johor Bahru', 'Johor Bahru'), ('Malacca City', 'Malacca City'), ('Alor Setar', 'Alor Setar'), ('Kota Bharu', 'Kota Bharu'), ('Kuala Terengganu', 'Kuala Terengganu'), ('Kuantan', 'Kuantan'), ('Seremban', 'Seremban'), ('Kuching', 'Kuching'), ('Miri', 'Miri'), ('Kota Kinabalu', 'Kota Kinabalu'), ('Sandakan', 'Sandakan'), ('Tawau', 'Tawau')], max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='required_education',
            field=models.CharField(blank=True, choices=[('High School', 'High School'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Doctorate', 'Doctorate')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='languageproficiency',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Mandarin', 'Mandarin'), ('Malay', 'Malay'), ('Tamil', 'Tamil'), ('Spanish', 'Spanish'), ('French', 'French'), ('German', 'German'), ('Japanese', 'Japanese'), ('Korean', 'Korean'), ('Arabic', 'Arabic')], max_length=100),
        ),
        migrations.AlterField(
            model_name='preferredjobclassification',
            name='job_classification',
            field=models.CharField(choices=[('Engineering', 'Engineering'), ('Data & Analytics', 'Data & Analytics'), ('Product Management', 'Product Management'), ('Design', 'Design'), ('Marketing', 'Marketing'), ('Sales', 'Sales'), ('Human Resources', 'Human Resources'), ('Finance', 'Finance'), ('Customer Support', 'Customer Support')], max_length=255),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(choices=[('Programming', 'Programming'), ('Data Analysis', 'Data Analysis'), ('Project Management', 'Project Management'), ('Graphic Design', 'Graphic Design'), ('Digital Marketing', 'Digital Marketing'), ('Sales', 'Sales'), ('Customer Service', 'Customer Service'), ('Content Writing', 'Content Writing'), ('Public Speaking', 'Public Speaking'), ('Problem Solving', 'Problem Solving')], max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='home_location',
            field=models.CharField(choices=[('Kuala Lumpur', 'Kuala Lumpur'), ('George Town', 'George Town'), ('Ipoh', 'Ipoh'), ('Shah Alam', 'Shah Alam'), ('Petaling Jaya', 'Petaling Jaya'), ('Johor Bahru', 'Johor Bahru'), ('Malacca City', 'Malacca City'), ('Alor Setar', 'Alor Setar'), ('Kota Bharu', 'Kota Bharu'), ('Kuala Terengganu', 'Kuala Terengganu'), ('Kuantan', 'Kuantan'), ('Seremban', 'Seremban'), ('Kuching', 'Kuching'), ('Miri', 'Miri'), ('Kota Kinabalu', 'Kota Kinabalu'), ('Sandakan', 'Sandakan'), ('Tawau', 'Tawau')], max_length=255),
        ),
    ]
