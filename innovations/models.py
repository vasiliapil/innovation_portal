from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

class Innovation(models.Model):
  Επιλογή_επίπεδο= (("Τοπικό", "Τοπικό"), ("Περιφερειακό", "Περιφερειακό"), ("Κεντρικό", "Κεντρικό")) 
  Επιλογή_τομέα= (("Δημοσία Διακυβέρνηση", "Δημοσία Διακυβέρνηση"), ("Οικονομία", "Οικονομία"), ("Υγεία", "Υγεία"), ("Κοινωνική Πολιτική", "Κοινωνική Πολιτική"), ("Εκπαίδευση", "Εκπαίδευση"), ("Περιβάλλον","Περιβάλλον"), ("Πολιτική Προστασία", "Πολιτική Προστασία"), ("Τουρισμός", "Τουρισμός"), ("Πολιτισμός και Αθλητισμός", "Πολιτισμός και Αθλητισμός"), ("Αγροτική Ανάπτυξη", "Αγροτική Ανάπτυξη"), ("Άλλο", "Άλλο"))
  Επιλογή_τύπος= (("Υπηρεσία", "Υπηρεσία"), ("Οργάνωση", "Οργάνωση"), ("Διαδικασία", "Διαδικασία"), ("Συμμετοχή πολιτών", "Συμμετοχή πολιτών"))
  Επιλογή_στάδιο= (("Σχεδιασμός", "Σχεδιασμός"), ("Πειραματική εφαρμογή", "Πειραματική εφαρμογή"),  ("Εφαρμογή", "Εφαρμογή"), ("Διάδοση", "Διάδοση"))
  Τίτλος =   models.CharField(max_length=255)
  network_member= models.ForeignKey("users.Network_member", related_name="network_member",blank= True, null=True, on_delete= models.CASCADE)
  timestamp= models.DateTimeField(auto_now_add=True)
  Φορέας = models.CharField(max_length=255)
  Επίπεδο = models.CharField(max_length=400, choices= Επιλογή_επίπεδο, null=True)
  Περιγραφή= models.CharField(max_length=2000, default="")
  Τομέας= models.CharField(max_length=400, choices= Επιλογή_τομέα, null=True)
  Τύπος = models.CharField(max_length=400, choices= Επιλογή_τύπος, null=True)
  Στάδιο = models.CharField(max_length=400, choices= Επιλογή_στάδιο, null=True)
  Στόχοι= models.CharField(max_length=2000, default= "")
  Αποτελέσματα= models.CharField(max_length=2000, default= "")
  Σχεδιασμός = models.CharField(max_length=2000)
  Πειραματική_εφαρμογή= models.CharField(max_length=2000)
  Εφαρμογή= models.CharField(max_length=2000)
  Διάδοση= models.CharField(max_length=2000)
  Χρηματοδότηση= models.CharField(max_length=2000)
  history= HistoricalRecords()
  
  def __str__(self):
    return f"{self.Τίτλος} {self.Φορέας}"
  
  def innovation_save(self):
    innovation= Innovation.save(self)
  
  def get_absolute_url(self):
        return reverse('innov_details', kwargs={'id': self.pk})