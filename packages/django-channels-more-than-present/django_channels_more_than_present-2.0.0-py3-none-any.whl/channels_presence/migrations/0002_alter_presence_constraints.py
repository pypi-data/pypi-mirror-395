# Generated migration to replace unique_together with constraints

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels_presence', '0001_initial'),
    ]

    operations = [
        # Remove old unique_together
        migrations.AlterUniqueTogether(
            name='presence',
            unique_together=set(),
        ),
        # Add new constraint
        migrations.AddConstraint(
            model_name='presence',
            constraint=models.UniqueConstraint(
                fields=['room', 'channel_name'],
                name='unique_presence_room_channel'
            ),
        ),
    ]
