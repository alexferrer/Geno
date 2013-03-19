'''
Created on Nov 19, 2010

@author: alex
'''
import os
global out

def show(node):
    global out
    print >>out , '%s [label="%s\l %s\l %s\l %s"];' % (node.pk,
                   node.pk,
                   node.nombre.encode("utf-8"),
                   node.a_paterno.encode("utf-8"),
                   node.a_materno.encode("utf-8"))

    if node.madre:
       print >>out ,  node.madre.pk , '->', node.pk

    if node.padre and node.madre :
       print >>out , node.padre.pk, '->', node.madre.pk, '[color=blue];'

def draw(node):
    global out
    # the /var/www/ is needed so the system can compute the graph
    # later it will be changed to the relative server location
    image = '/var/www/media/'+str(node.foto)
    
    if not node.foto :
        print >>out , '%s [label="%s\l %s\l %s\l %s"];' % (node.pk,
                   node.pk,
                   node.nombre.encode("utf-8"),
                   node.a_paterno.encode("utf-8"),
                   node.a_materno.encode("utf-8"))
    else :
        print >>out , '%s [label="\l \l \l" image="%s"];' % (node.pk, image)

    if node.madre:
       print >>out ,  node.madre.pk , '->', node.pk

    if node.padre and node.madre :
       print >>out , node.padre.pk, '->', node.madre.pk, '[color=blue];'
    
 
def process(nodos):
    global out 
    out = open('/home/alex/djcode/myproject/geno/tree.dot','w')

    print >>out ,' digraph graphname { '
    print >>out ,'ratio="0.23";' # separation between ranges 13
    print >>out ,'size="100,129"'
    #[draw(n)  for n in nodos] 
    [show(n)  for n in nodos] 
    print >>out , '}'    
    out.close()
    os.system('/usr/bin/dot -Tsvg -o/home/alex/djcode/myproject/geno/famtree.svg /home/alex/djcode/myproject/geno/tree.dot')    
    # for image graphs only, replace all 
    #sed 's/\/var\/www//g' famtree.svg > famtreeg.svg
    # I am assuming that the realative (www.ftconsult.com) will be spared
    #os.system('s/\/var\/www//g' '/home/alex/djcode/myproject/geno/famtree.svg' '/home/alex/djcode/myproject/geno/famtreeg.svg')