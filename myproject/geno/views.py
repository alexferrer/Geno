# Create your views here.
from django.contrib.auth.decorators import login_required

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.context_processors import request
from django.shortcuts import render_to_response
#, redirect
from myproject.geno.models import Nodo
import myproject.geno.graph
from myproject.geno.genolib import get_person_by_pk,get_siblings,get_children,get_spouse
from myproject.geno.genolib import addfamily_from_pk,addspousekids, addkids,addparent
from myproject.geno.forms import PersonForm
from myproject.geno.forms import FamilyForm
from myproject.geno.forms import SpouseKidsForm, KidsForm, ParentForm, EasyPersonForm
# -------------------

from django.contrib.auth import authenticate, login


def hello(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            #cd = form.cleaned_data
            #print cd['nombre']
            return HttpResponse('form submitted')
    else:
        form = PersonForm(
               initial={'a_materno':'initial stuff'}
                          )
    return render_to_response('contact_form.html',{'form':form} )
         
def hola(request):
    if request.user.is_authenticated():
      author = request.user.username
      message = "Usted, %s esta autorizado a visitar esta pagina, bienvenido",author
    else:
      message = "Esta pagina es privada y usted No esta autorizado a visitar.<br>"
      
    return render_to_response('index.html',{'message':message} )

@login_required 
def maketree(request):
    myproject.geno.graph.process(Nodo.objects.all())
    return HttpResponseRedirect('/media/geno/famtree.svg') 
    #return HttpResponseRedirect('/media1/geno/famtree.svg') #FOR LOCAL SERVER ONLY

@login_required 
def addfamily(request):
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            author=request.user.username
            f=form.cleaned_data['father_pk']
            m=form.cleaned_data['mother_pk']
            l=form.cleaned_data['child1']
            addfamily_from_pk(f,m,l)
            return HttpResponse('Family added'+l)
    else:
        form = FamilyForm()

    return render_to_response('add_family_form.html',{'form':form} )

@login_required     
def add_spouse_and_kids(request):
    key     = request.GET.get('key')
    person  = get_person_by_pk( int( key ) )
    
    if request.method == 'POST':
        form = SpouseKidsForm(request.POST)
        if form.is_valid(): 
            author=request.user.username
            spouse_name  = form.cleaned_data['nombre']
            spouse_last1 = form.cleaned_data['apellido_paterno']
            spouse_last2 = form.cleaned_data['apellido_materno']
            gender  = form.cleaned_data['relacion']
            kids    = form.cleaned_data['kids']
            addspousekids(author,key,spouse_name,spouse_last1,spouse_last2,gender,kids)
            return HttpResponseRedirect('/show_person/'+str(key))
    else:
        form = SpouseKidsForm()

    return render_to_response('add_family_form.html',{'form':form ,'key':key, 'person':person} ) 

@login_required 
def add_kids(request):
    key     = request.GET.get('key')
    person  = get_person_by_pk( int( key ) )
    
    if request.method == 'POST':
        form = KidsForm(request.POST)
        if form.is_valid():
            author  = request.user.username
            kids    = form.cleaned_data['kids']
            addkids(author,key ,kids)
            return HttpResponseRedirect('/show_person/'+str(key))
    else:
        form = KidsForm()

    return render_to_response('add_kids_form.html',{'form':form,'key':key,'person':person} ) 

@login_required 
def add_parent(request):
    key      = request.GET.get('key')
    person   = get_person_by_pk( int( key ) )
    relacion = request.GET.get('relacion')

    #if relacion = 'Padre' :
    #   select all for apellidopadre lastname
    # else 
    #   select all for apellidomadre
    # make into choicelist
       
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            author = request.user.username
            nombre    = form.cleaned_data['nombre']
            apellido_paterno = form.cleaned_data['apellido_paterno']
            apellido_materno = form.cleaned_data['apellido_materno']
            addparent(author,key ,nombre,apellido_paterno,apellido_materno,relacion)
            return HttpResponseRedirect('/show_person/'+str(key))
    else:
        form = ParentForm()

    return render_to_response('add_parent_form.html',{'form':form,'key':key,'person':person,'relacion':relacion} ) 
    
    
@login_required     
def show_person(request,nodo):
    try:     # select the person from the incoming form 
        nodo = int(nodo)
    except ValueError:
        raise Http404()

    person       = get_person_by_pk(nodo) 
    sibling_list = get_siblings(person)
    child_list   = get_children(person)
    spouse_list  = get_spouse(person)
    
    #locals passes all variables to the template                              )
    return render_to_response('show_person.html', locals())

@login_required    
def edit_person(request):
    key      = request.GET.get('key')
    person   = get_person_by_pk( int( key ) )

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            author=request.user.username
            person.nombre           = form.cleaned_data['nombre']
            person.apellido_paterno = form.cleaned_data['a_paterno']
            person.apellido_materno = form.cleaned_data['a_materno']
            
            padre                   = form.cleaned_data['padre']
            madre                   = form.cleaned_data['madre']
            
            if padre :
               person.padre = get_person_by_pk( int(padre) )
               
            if madre :              
               person.madre = get_person_by_pk( int( madre ) )
             
            person.dob              = form.cleaned_data['dob']
            person.gender           = form.cleaned_data['gender']
            person.foto             = form.cleaned_data['foto']
            # do the save or whatever here
            person.logged_save(author)
            return HttpResponseRedirect('/show_person/'+str(key))
    else:
        form = PersonForm(initial={'nombre': person.nombre,
                                   'a_paterno': person.a_paterno,
                                   'a_materno': person.a_materno,
                                   'padre'    : person.padre.pk,
                                   'madre'    : person.madre.pk,
                                   'dob'      : person.dob,
                                   'gender'   : person.gender,
                                   'foto'     : person.foto
                                   })

    return render_to_response('edit_person_form.html',{'form':form,'key':key,'person':person} ) 

@login_required    
def easy_edit_person(request):
    key      = request.GET.get('key')
    person   = get_person_by_pk( int( key ) )

    if request.method == 'POST':
        author=request.user.username
        form = EasyPersonForm(request.POST,instance=person)
        form.save(commit=False) # save the form to the node, but not the node itself
        person.logged_save(author)
        return HttpResponseRedirect('/show_person/'+str(key))
    else:
        form = EasyPersonForm(instance=person)

    return render_to_response('edit_person_form.html',{'form':form,'key':key,'person':person} ) 

                
