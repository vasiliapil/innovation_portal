# Generated by Django 4.2.11 on 2024-05-22 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Innovation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Τίτλος', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Φορέας', models.CharField(max_length=255)),
                ('Επίπεδο', models.CharField(choices=[('Τοπικό', 'Τοπικό'), ('Περιφερειακό', 'Περιφερειακό'), ('Κεντρικό', 'Κεντρικό')], max_length=400, null=True)),
                ('Περιγραφή', models.CharField(default='', max_length=2000)),
                ('Τομέας', models.CharField(choices=[('Δημοσία Διακυβέρνηση', 'Δημοσία Διακυβέρνηση'), ('Οικονομία', 'Οικονομία'), ('Υγεία', 'Υγεία'), ('Κοινωνική Πολιτική', 'Κοινωνική Πολιτική'), ('Εκπαίδευση', 'Εκπαίδευση'), ('Περιβάλλον', 'Περιβάλλον'), ('Πολιτική Προστασία', 'Πολιτική Προστασία'), ('Τουρισμός', 'Τουρισμός'), ('Πολιτισμός και Αθλητισμός', 'Πολιτισμός και Αθλητισμός'), ('Αγροτική Ανάπτυξη', 'Αγροτική Ανάπτυξη'), ('Άλλο', 'Άλλο')], max_length=400, null=True)),
                ('Τύπος', models.CharField(choices=[('Υπηρεσία', 'Υπηρεσία'), ('Οργάνωση', 'Οργάνωση'), ('Διαδικασία', 'Διαδικασία'), ('Συμμετοχή πολιτών', 'Συμμετοχή πολιτών')], max_length=400, null=True)),
                ('Στάδιο', models.CharField(choices=[('Σχεδιασμός', 'Σχεδιασμός'), ('Πειραματική εφαρμογή', 'Πειραματική εφαρμογή'), ('Εφαρμογή', 'Εφαρμογή'), ('Διάδοση', 'Διάδοση')], max_length=400, null=True)),
                ('Στόχοι', models.CharField(default='', max_length=2000)),
                ('Αποτελέσματα', models.CharField(default='', max_length=2000)),
                ('Σχεδιασμός', models.CharField(max_length=2000)),
                ('Πειραματική_εφαρμογή', models.CharField(max_length=2000)),
                ('Εφαρμογή', models.CharField(max_length=2000)),
                ('Διάδοση', models.CharField(max_length=2000)),
                ('Χρηματοδότηση', models.CharField(max_length=2000)),
                ('network_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='network_member', to='users.network_member')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInnovation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('Τίτλος', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(blank=True, editable=False)),
                ('Φορέας', models.CharField(max_length=255)),
                ('Επίπεδο', models.CharField(choices=[('Τοπικό', 'Τοπικό'), ('Περιφερειακό', 'Περιφερειακό'), ('Κεντρικό', 'Κεντρικό')], max_length=400, null=True)),
                ('Περιγραφή', models.CharField(default='', max_length=2000)),
                ('Τομέας', models.CharField(choices=[('Δημοσία Διακυβέρνηση', 'Δημοσία Διακυβέρνηση'), ('Οικονομία', 'Οικονομία'), ('Υγεία', 'Υγεία'), ('Κοινωνική Πολιτική', 'Κοινωνική Πολιτική'), ('Εκπαίδευση', 'Εκπαίδευση'), ('Περιβάλλον', 'Περιβάλλον'), ('Πολιτική Προστασία', 'Πολιτική Προστασία'), ('Τουρισμός', 'Τουρισμός'), ('Πολιτισμός και Αθλητισμός', 'Πολιτισμός και Αθλητισμός'), ('Αγροτική Ανάπτυξη', 'Αγροτική Ανάπτυξη'), ('Άλλο', 'Άλλο')], max_length=400, null=True)),
                ('Τύπος', models.CharField(choices=[('Υπηρεσία', 'Υπηρεσία'), ('Οργάνωση', 'Οργάνωση'), ('Διαδικασία', 'Διαδικασία'), ('Συμμετοχή πολιτών', 'Συμμετοχή πολιτών')], max_length=400, null=True)),
                ('Στάδιο', models.CharField(choices=[('Σχεδιασμός', 'Σχεδιασμός'), ('Πειραματική εφαρμογή', 'Πειραματική εφαρμογή'), ('Εφαρμογή', 'Εφαρμογή'), ('Διάδοση', 'Διάδοση')], max_length=400, null=True)),
                ('Στόχοι', models.CharField(default='', max_length=2000)),
                ('Αποτελέσματα', models.CharField(default='', max_length=2000)),
                ('Σχεδιασμός', models.CharField(max_length=2000)),
                ('Πειραματική_εφαρμογή', models.CharField(max_length=2000)),
                ('Εφαρμογή', models.CharField(max_length=2000)),
                ('Διάδοση', models.CharField(max_length=2000)),
                ('Χρηματοδότηση', models.CharField(max_length=2000)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('network_member', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.network_member')),
            ],
            options={
                'verbose_name': 'historical innovation',
                'verbose_name_plural': 'historical innovations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
