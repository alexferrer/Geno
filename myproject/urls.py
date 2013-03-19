from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login
from geno.views import hello,hola,maketree,addfamily,add_spouse_and_kids
from geno.views import add_parent,show_person,add_kids, edit_person, easy_edit_person

from django.contrib import databrowse
from geno.models import Nodo
databrowse.site.register(Nodo)

admin.autodiscover()

urlpatterns = patterns('',
     (r'^editperson/', easy_edit_person),
     (r'^addparent/', add_parent), 
     (r'^addspousekids/', add_spouse_and_kids),  
     (r'^addkids/', add_kids),               
     (r'^hello/', hello),
     (r'^$', hola),
     (r'^show_person/(\d+)/$',show_person),    #los parentecis indican la variable capturada

     (r'^addfamily/', addfamily),
     (r'^maketree/', maketree),
     (r'^admin/(.*)', admin.site.root),
          
     (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/alex/workspace/Pyjama/src'}),
     # this is the JSONRPC service line that needs to be added:
     #(r'^test-service/$', 'myproject.geno.views.testservice'),

     (r'^databrowse/(.*)', databrowse.site.root),

)


