from django import forms
from django.forms import ModelForm
from .models import Innovation

class InnovationForm(ModelForm):
    class Meta:
        model = Innovation
        fields= ("Τίτλος", "Φορέας", "Επίπεδο", "Περιγραφή", "Τομέας", "Τύπος", "Στάδιο", "Στόχοι", "Αποτελέσματα", "Σχεδιασμός", "Πειραματική_εφαρμογή", "Εφαρμογή", "Διάδοση", "Χρηματοδότηση")
        
class InnovationSearchForm(forms.Form):
  Επιλογή_επίπεδο= (("Τοπικό", "Τοπικό"), ("Περιφερειακό", "Περιφερειακό"), ("Κεντρικό", "Κεντρικό")) 
  Επιλογή_τομέα= (("Δημοσία Διακυβέρνηση", "Δημοσία Διακυβέρνηση"), ("Οικονομία", "Οικονομία"), ("Υγεία", "Υγεία"), ("Κοινωνική Πολιτική", "Κοινωνική Πολιτική"), ("Εκπαίδευση", "Εκπαίδευση"), ("Περιβάλλον","Περιβάλλον"), ("Πολιτική Προστασία", "Πολιτική Προστασία"), ("Τουρισμός", "Τουρισμός"), ("Πολιτισμός και Αθλητισμός", "Πολιτισμός και Αθλητισμός"), ("Αγροτική Ανάπτυξη", "Αγροτική Ανάπτυξη"), ("Άλλο", "Άλλο"))
  Επιλογή_τύπος= (("Υπηρεσία", "Υπηρεσία"), ("Οργάνωση", "Οργάνωση"), ("Διαδικασία", "Διαδικασία"), ("Συμμετοχή πολιτών", "Συμμετοχή πολιτών"))
  Τίτλος =  forms.CharField(max_length=255, required=False)
  Φορέας = forms.CharField(max_length=255, required=False)
  Επίπεδο = forms.MultipleChoiceField(choices= Επιλογή_επίπεδο, required=False)
  Τομέας= forms.MultipleChoiceField(choices= Επιλογή_τομέα, required=False)
  Τύπος = forms.MultipleChoiceField(choices= Επιλογή_τύπος, required=False)
  Ημερομηνία_δημοσίευσης_από= forms.DateField(
    widget=forms.DateInput(
      attrs={"class": "form-control","type":"date"}), required=False)
  Ημερομηνία_δημοσίευσης_μέχρι= forms.DateField(
    widget=forms.DateInput(
      attrs={"class": "form-control","type":"date"}), required=False)
  
