from django import forms
from myproject.geno.models import Nodo
from django.core.exceptions import ObjectDoesNotExist

from django.forms import ModelForm

class EasyPersonForm(ModelForm):
    class Meta:
        model = Nodo
     
class PersonForm(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'))

    nombre    = forms.CharField(label='Nombres')
    a_paterno = forms.CharField(label='Apellido Paterno',required=True)
    a_materno = forms.CharField(label='Apellido Materno',required=False)
    dob       = forms.DateField(label="Fecha Nacimiento",required=False)
    dod       = forms.DateField(label="Fecha Defuncion",required=False)
    gender    = forms.ChoiceField(label="Sexo",choices=GENDER_CHOICES,required=True)
    foto      = forms.ImageField( help_text="Should be 100px by 100px size",required=False)
    padre     = forms.CharField(label='Padre',required=False)
    madre     = forms.CharField(label='Madre',required=False,widget=forms.Select(choices=GENDER_CHOICES) )
    
    

    def clean_padre(self):
        padre  = self.cleaned_data['padre']
        if not padre:
            return False
        
        try:     
            padre = int(padre)
        except ValueError:
            raise forms.ValidationError("ingrese el numero de nodo del padre")
        return padre

    def clean_madre(self):
        madre  = self.cleaned_data['madre']
        if not madre:
            return False

        try:     
            madre = int(self.cleaned_data['madre'])
        except ValueError:
            raise forms.ValidationError("ingrese el numero de nodo de la madre")
        return madre

class FamilyForm(forms.Form):
    father_pk = forms.IntegerField()
    mother_pk = forms.IntegerField()
    child1 = forms.CharField()

    def clean_father_pk(self):
        key = self.cleaned_data['father_pk']
        self.validate_key(key)
        return key

    def clean_mother_pk(self):
        key = self.cleaned_data['mother_pk']
        self.validate_key(key)
        return key

    def validate_key(self,key):
        ''' validate that the keys do exists '''
        try:
            per = Nodo.objects.get(pk=key)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Person key does not exists!!")

class SpouseKidsForm(forms.Form):
    GENDER_CHOICES = (
        ('Male', 'Marido'),
        ('Female', 'Mujer'))

    nombre  = forms.CharField()
    apellido_paterno = forms.CharField()
    apellido_materno = forms.CharField()
    relacion     = forms.ChoiceField(required=True,choices=GENDER_CHOICES)
    kids         = forms.CharField()
    
 
class KidsForm(forms.Form):
    kids         = forms.CharField()
    
class ParentForm(forms.Form):
    nombre  = forms.CharField()
    apellido_paterno = forms.CharField()
    apellido_materno = forms.CharField()
    