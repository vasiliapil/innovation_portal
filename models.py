from django.db import models

from django.contrib.auth.models import User




class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Δημιουργήθηκε = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)   
   

class Network_member(models.Model):
    
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    Όνομα = models.CharField(max_length=30)
    Επώνυμο = models.CharField(max_length=30)
    Φορέας_εργασίας = models.CharField(max_length=50)
    Ιδιότητα = models.CharField(max_length=150)
    Τηλέφωνο= models.CharField(max_length= 30)
    
    
    def __str__(self):
       return f"{self.Όνομα} {self.Επώνυμο}"
   


