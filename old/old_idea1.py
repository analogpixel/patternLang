#!/usr/bin/env python
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing import matplotlib
from math import *
import copy

class Shape():
    def __init__(self, shapeType, pts=[]):
        self.o = shapeType
        self.pts = pts
    def __str__(self):
        return "Object: {} points: {}".format( self.o, self.pts)

# rotate object o around a circle divied into n sections
# returns n objects
# TODO: should return a group 
def radial_sym(o, n,offset=0): 
    r = []

    for obj in o:
        if type(obj) == list:
            r.append ( radial_sym(obj, n , offset) )
        else:
            _d = int(360/n) 
            r.append([ rotate(x, obj) for x in range(offset,360-offset,_d) ] )
    return r

## x,y are the center of the rect
def rect(x,y,w,h):
    return Shape('rect', pts=[ (x-(w/2), y-(h/2)), (x+(w/2), y-(h/2)), (x+(w/2), y+(h/2)), (x-(w/2), y+(h/2)) ] )

def ellipse(x,y,w,h):
    # the second argument is a vector in which direction the ellipse points
    e= Shape('ellipse', pts=[(x,y),(0,1)])
    # e.ratio = 0.5
    e.ratio = 1
    return e

def translate(_o, _x,_y):
    r = []
    for obj in _o:
        if type(obj) == list:
            r.append( translate(obj, _x,_y))
        else:
            o = copy.deepcopy(obj)
            o.pts = [ (_x+x, _y+y) for x,y in o.pts ]
            r.append(o)
    return r

def rotate(deg, _o):
    o = copy.deepcopy(_o)
    _d = deg * (pi/180)
    o.pts = [ ( (cos(_d) * x - sin(_d) * y),  (sin(_d) * x + cos(_d) * y) ) for x,y in o.pts ]
    return o

def render(o):
    doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
    msp = doc.modelspace()  # add new entities to the modelspace
    _render(msp,o)
    doc.saveas('line.dxf')
    matplotlib.qsave(doc.modelspace(), 'out.png')

def _render(msp, o):
    for obj in o:
        ## recurse into groups
        if type(obj) == list:
            _render(msp,obj)
        ## otherwise render the object
        else:
            print(obj)
            # TODO : render box from center 
            if obj.o == 'rect':
                hatch = msp.add_hatch(color=3)
                hatch.paths.add_polyline_path(obj.pts, is_closed=1) 
            if obj.o == 'ellipse':
                hatch = msp.add_hatch(color=2)
                edge_path = hatch.paths.add_edge_path()
                edge_path.add_ellipse( ( obj.pts[0][0], obj.pts[0][1]) , major_axis=(obj.pts[1][0], obj.pts[1][1]), ratio=obj.ratio )

pattern = []

# r = rect(0,10, 1,5)
# e = ellipse(0,10, 10,10)
# pattern.append( [ellipse(-10,-10, 10,10), ellipse(10,-10,10,10), ellipse(10,10,10,10), ellipse(-10,10,10,10) ] )
circs = [ellipse(-10,-10, 15,15), ellipse(10,10,10,10)]  
# circs = translate(circs,10,0)
pattern.append( circs )
pattern.append( ellipse(0,0,5,5) )

render(pattern)
