'''Created on Nov 19, 2010

@author: alex
library for genealogy research
'''
from myproject.geno.models import Nodo
from datetime import datetime

def get_person_by_pk(id):
    return Nodo.objects.get(pk=id)

def grandmother_father(person):
    return  person.padre.madre

def get_grandparents(person):
    return  (person.padre.madre,person.padre.padre,person.madre.madre,person.madre.padre)

def get_children(person):
    return Nodo.objects.filter(padre=person)|Nodo.objects.filter(madre=person)

def grandchildren(person):
    childlists = [get_children(h) for h in get_children(person)]
    return [item for sublist in childlists for item in sublist] #flaten the lists
  
def get_siblings(person):
    if person.madre and person.padre:
        return Nodo.objects.filter(madre=person.madre).exclude(id=person.id) |  Nodo.objects.filter(padre=person.padre).exclude(id=person.id)
    if person.madre :
        return Nodo.objects.filter(madre=person.madre).exclude(id=person.id)
    if person.padre:
        return Nodo.objects.filter(padre=person.padre).exclude(id=person.id)

def get_spouse(person):
    childs = get_children(person)
    spouse_list=[]
    if not childs :
        return spouse_list
    
    if childs[0].padre == person :  # person is the father
        spouse_list= [each.madre for each in childs]
    else:
        spouse_list= [each.padre for each in childs]
            
    return set(spouse_list)
    
def addfamily(author,father,mother,child_names):
    ''' father,mother, list of child names '''
    for name in child_names:
        new_child = Nodo(padre=father,
                         madre=mother,
                         nombre=name,
                         a_paterno=father.a_paterno,
                         a_materno=mother.a_paterno,
                         dob=datetime.now())
        
        new_child.logged_save(author)

def addfamily_from_pk(author,fatherkey,motherkey,csvlist):
    p = get_person_by_pk(fatherkey)
    m = get_person_by_pk(motherkey)
    addfamily(author,p,m,csvlist.split(','))

def addperson(author,name,last1,last2):
    new_person = Nodo(nombre=name,
                      a_paterno=last1,
                      a_materno=last2,
                      dob=datetime.now())
    new_person.logged_save(author)
    return new_person

def addspousekids(author,person_key,spouse_name,spouse_last1,spouse_last2,gender,kids):
    parent_a = get_person_by_pk(person_key)
    parent_b = addperson(author,spouse_name,spouse_last1,spouse_last2)
    childs   = kids.split(',')
    
    if not childs:
        childs = ['none']
        
    if gender == 'Female':
        addfamily(author,parent_a,parent_b,childs)
    else:
        addfamily(author,parent_b,parent_a,childs)
       
def addkids(author,child_key,csvlist):
    child     = get_person_by_pk(child_key)
    fatherkey = child.padre.pk
    motherkey = child.madre.pk
    addfamily_from_pk(author,fatherkey,motherkey,csvlist)

def addparent(author,key ,nombre,apellido_paterno,apellido_materno,relacion) :
    child     = get_person_by_pk(key)
    parent    = addperson(author,nombre,apellido_paterno,apellido_materno)
    if relacion == 'Padre':
        child.padre = parent
    else:
        child.madre = parent
    
    child.logged_save(author)