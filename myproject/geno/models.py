from django.db import models
from datetime import datetime

          
class Nodo(models.Model):
    GENDER_CHOICES = ((u'M',u"Male"),(u'F',u'Female'))
    
    nombre = models.CharField(max_length=30)
    a_paterno = models.CharField(max_length=20,blank=True,null=True)
    a_materno = models.CharField(max_length=20,blank=True,null=True)
    padre  = models.ForeignKey('self',blank=True,null=True,related_name="paterno")
    madre  = models.ForeignKey('self',blank=True,null=True,related_name="materno")
    dob    = models.DateField(blank=True,null=True)
    #dod    = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=1,blank=True,null=True,choices=GENDER_CHOICES)
    foto = models.ImageField(upload_to="geno/images", blank=True, help_text="Should be 100px by 100px size")


    def year_born(self):
        return self.dob.year
      
    def __unicode__(self):
        return u'%s %s %s' % (self.nombre,self.a_paterno,self.a_materno)

    def logged_save(self,user):
        # save nodo first, so to get nodeid
        self.save()      

        # now save nodo on NodoLog
        
        father=None
        mother=None
        if self.padre:
            father = self.padre.pk
        if self.madre:
            mother = self.madre.pk

            
        # now save the historical record
        nodo_log = NodoLog(nodo_id   = self.pk,
                           nombre    = self.nombre,        # save nodo
                           a_paterno = self.a_paterno,
                           a_materno = self.a_materno,
                           padre     = father,
                           madre     = mother,
                           dob       = self.dob,
                           gender    = self.gender,
                           foto      = self.foto.name,
                           ingreso   = datetime.now(),
                           author    = user
                          )
        nodo_log.save()
      
class NodoLog(models.Model):
    nodo_id   = models.IntegerField()
    nombre    = models.CharField(max_length=30,blank=True,null=True)
    a_paterno = models.CharField(max_length=20,blank=True,null=True)
    a_materno = models.CharField(max_length=20,blank=True,null=True)
    padre   = models.IntegerField(blank=True,null=True)
    madre   = models.IntegerField(blank=True,null=True)
    dob     = models.DateField(blank=True,null=True)
    dod     = models.DateField(blank=True,null=True)
    gender  = models.CharField(max_length=1,blank=True,null=True)
    foto    = models.CharField(max_length=100,blank=True,null=True)
    ingreso = models.DateTimeField()
    author  = models.CharField(max_length=30)
      
    def __unicode__(self):
        return u'%s  > %s >>> %s %s %s' % (self.author,self.ingreso,self.nombre,self.a_paterno,self.a_materno)
      