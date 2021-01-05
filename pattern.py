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
    this.dwg.viewbox(0, 0, viewbox_tuple[0], viewbox_tuple[1])
    this.width = viewbox_tuple[0]
    this.height = viewbox_tuple[1]

def name( file_name):
    this.dwg.filename = file_name

def group( group_name):
    return this.dwg.g(id=group_name ) 

## TODO, take a list of object and add them all
def add( o ):
    this.dwg.add( o )

def save():
    this.dwg.save()

def rect( center_point, rect_size):
    x = center_point[0]
    y = center_point[1]
    w = rect_size[0]
    h = rect_size[1]
    _x = x - (w/2) + (this.width/2)  # center on screen, and place at center of rectangle
    _y = y - (h/2) + (this.height/2) # center on screen, and place at center of rectangle
    return this.dwg.rect(insert=( _x,_y), size=(w,h)) 
