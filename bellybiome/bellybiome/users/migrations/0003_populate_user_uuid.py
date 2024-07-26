# bellybiome/users/migrations/0003_populate_user_uuid.py
from django.db import migrations, models
import uuid

def generate_uuids(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.all():
        user.uuid = uuid.uuid4()
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_uuid'),
    ]

    operations = [
        migrations.RunPython(generate_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
 