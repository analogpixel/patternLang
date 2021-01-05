import svgwrite
from svgwrite import cm, mm   
import sys

this = sys.modules[__name__]

this.dwg = False
this.width = 0
this.height = 0
this.unit = "cm"

def unit(s):
    this.unit = s

def size( size_tuple, viewbox_tuple ):
    t =  tuple([ "{}{}".format(t,this.unit) for t in size_tuple ] )
    this.dwg = svgwrite.Drawing(name, debug=True, size=size_tuple)
    this.dwg.viewbox(-viewbox_tuple[0]/2, -viewbox_tuple[1]/2, viewbox_tuple[0], viewbox_tuple[1] )
    this.width = viewbox_tuple[0]
    this.height = viewbox_tuple[1]

def name( file_name):
    this.dwg.filename = file_name

def group( group_name):
    return this.dwg.g(id=group_name ) 

def add( *o ):
    for obj in o:    
        this.dwg.add( obj )
def save():
    this.dwg.save()

def rotate( deg,o):
    o.rotate(angle=deg, center=(this.width/2,this.height/2))
    return o

def translate(x,y,o):
    o.translate(x,y)
    return o

def rect( x,y,w,h):
    _x = x - (w/2)
    _y = y - (h/2)
    return this.dwg.rect(insert=( _x,_y), size=(w,h)) 
