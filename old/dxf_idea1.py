#!/usr/bin/env python

import svgwrite
#import ezdxf
#from ezdxf.addons.drawing import RenderContext, Frontend
#from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
#from ezdxf.addons.drawing import matplotlib
from math import *
import copy

class Group():
    def __init__(self, *objects):
        self.group = []
        self.name = "none"
        self.z = 0
        for o in objects:
            self.group.append(o)

    def z(self,v):
        self.z = v
        return self

    def items(self):
        return self.group

    def append(self,o):
        self.group.append(o)
        return self

    def translate(self,x,y):
        self._translate(x,y,self.group)
        return self

    def _translate(self,x,y,o):
        for obj in o:
            if type(obj) == Group:
                _translate(obj, x,y)
            else:
                obj.translate(x,y)
        return self

    def radial_sym(self, n,offset=0): 
        newGroup = []
        _d = int(360/n) 
        for obj in self.group:
            for j in range(offset,360-offset,_d):
                newObject = copy.deepcopy(obj)
                newObject.rotate(j)
                newGroup.append(newObject)

        self.group = newGroup
        return self

class Renderer():
    def __init__(self):
        self.doc = ezdxf.new('R2010')
        self.msp = self.doc.modelspace()
        self.root = Group() 

    def append(self, o):
        self.root.append(o)

    def render(self):
        self._render(self.root)
        self.doc.saveas('line.dxf')
        matplotlib.qsave(self.doc.modelspace(), 'out.png')

    def _render(self, o):
        for obj in o.items():
            print( type(obj) )
            if type(obj) == Group:
                self._render( obj)
            ## otherwise render the object
            else:
                obj.draw(self.msp)

class Shape():
    def __init__(self):
        self.pts = pts
    def set(self, key,value):
        setattr(self, key, value)
        return self
    def translate(self,_x,_y):
        self.pts =[ (_x+x, _y+y) for x,y in self.pts ]
        return self

class Rect(Shape):
    def __init__(self,x,y,w,h):
        self.pts = [ (x-(w/2), y-(h/2)), (x+(w/2), y-(h/2)), (x+(w/2), y+(h/2)), (x-(w/2), y+(h/2)) ]
        self.o = 'rect'
        self.w = w
        self.h = h
    def draw(msp):
        hatch = msp.add_hatch(color=3)
        hatch.paths.add_polyline_path(self.pts, is_closed=1) 
        return self
    def rotate(self,_d):
        _d = _d * (pi/180)
        self.pts = [ ( (cos(_d) * x - sin(_d) * y),  (sin(_d) * x + cos(_d) * y) ) for x,y in self.pts ]
        return self

class Ellipse(Shape):
    def __init__(self,x,y,w,h):
        self.pts=[(x,y)]
        self.w=w
        self.h=h
        self.r=0
        self.ratio = 1
        self.color=2
    def draw(self,msp):
        hatch = msp.add_hatch(color=self.color)
        edge_path = hatch.paths.add_edge_path()
        edge_path.add_ellipse( ( self.pts[0][0], self.pts[0][1]) , major_axis=(self.w, self.h), ratio=self.ratio )
        return self
    def rotate(self,_d):
         _d = _d * (pi/180)
         self.r += _d
         self.pts = [ ( (cos(_d) * x - sin(_d) * y),  (sin(_d) * x + cos(_d) * y) ) for x,y in self.pts ]
         return self

# rotate object o around a circle divied into n sections
# returns n objects
# TODO: should return a group 

r = Renderer()
#circs = Group( Ellipse(-10,-10, 15,15), Ellipse(10,10,10,10) ) 
#circs.radial_sym(5)

"""
c = Group( Ellipse(20,0, 2,2) )
c.radial_sym(8)
c.translate(40,0)
c.radial_sym(4)
r.append( c )
"""

r.append(  Group( Ellipse(20,0,2,5).set('ratio', 0.5 ) ).radial_sym(8).translate(40,0).radial_sym(4) )
e = Ellipse(0,0,5,5)
e.color = 10
r.append( e)
r.render()
