#!/usr/bin/env python

import svgwrite
from math import *
import copy

ID=1
G_WIDTH=800
G_HEIGHT=800

class Group():
    def __init__(self, *objects):
        global ID
        self.group = []
        self.name = "id_" + str(ID)
        ID += 1
        self.z = 0
        self.fillColor = None
        for o in objects:
            self.group.append(o)

    def set_name(self):
        global ID
        self.name = "id_" + str(ID)
        ID += 1
        
    def z(self,v):
        self.z = v
        return self

    def fill(self, _fill):
        self.fillColor = _fill
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
                self._translate(x,y,obj.items())
            else:
                obj.translate(x,y)
        return self

    def radial_sym(self, n, offset=0):
        self._radial_sym(n, offset, self)
        return self

    def _radial_sym(self, n,offset, g): 
        newGroup = []
        _d = int(360/n) 

        for obj in g.group:
            if type(obj) == Group:
                 newGroup.append( self._radial_sym(n, offset, obj)  )
            else:
                for j in range(offset,360,_d):
                    j = (j + offset) % 360
                    newObject = copy.deepcopy(obj)
                    newObject.rotate(j)
                    newGroup.append(newObject)

        g.group = newGroup
        return g

class Renderer():
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.dwg = svgwrite.Drawing("out.svg", debug=True, size=(w,h))
        self.dwg.viewbox(0,0, w,h)
        self.root = Group() 

    def append(self, o):
        self.root.append(o)

    def render(self):
        rootGroup = self.dwg.g(id=self.root.name)
        rootGroup.translate(self.w/2, self.h/2)
        # ? rotate current group to group rotation  ?
        self._render(self.root, self.dwg.add( rootGroup ))
        self.dwg.save(pretty=True)

    def _render(self, o, currentGroup):
        # currentGroup = self.dwg.g( id=o.name )
        if o.fillColor:
            currentGroup.fill = o.fillColor
        
        for obj in o.items():
            if type(obj) == Group:
                tmp_g = currentGroup.add( self.dwg.g( id=obj.name) )
                self._render( obj, tmp_g)
            else:
                currentGroup.add( obj.draw(self.dwg) )

class Shape():
    def __init__(self):
        self.pts = pts
    def set(self, key,value):
        setattr(self, key, value)
        return self
    def translate(self,_x,_y):
        self.pts =[ (_x+x, _y+y) for x,y in self.pts ]
        return self

class Polygon(Shape):
    def __init__(self, pts):
        self.pts = pts
        self.r = 0
        self.fillColor='red'
    def draw(self,dwg):
        # group.add( dwg.polygon( points= self.pts , fill=self.fillColor))
        return dwg.polygon( points= self.pts , fill=self.fillColor)
    def rotate(self,_d):
        self.r += _d 
        _d = _d * (pi/180)
        self.pts = [ ( (cos(_d) * x - sin(_d) * y),  (sin(_d) * x + cos(_d) * y) ) for x,y in self.pts ]
        return self

def rect(w,h):
    x=0
    y=0
    pts = [ (x-(w/2), y-(h/2)), (x+(w/2), y-(h/2)), (x+(w/2), y+(h/2)), (x-(w/2), y+(h/2)) ]
    tmp = Polygon(pts)
    tmp.w = w
    tmp.h = h
    tmp.o = 'rect'
    return tmp


def triangle(b,h):
    x = 0
    y = 0
    pts = [ (x+(-b/2), y+(h/2)), (x+(b/2), y+(h/2)), (x, y+(-h/2)) ]
    tmp = Polygon(pts)
    tmp.b = b
    tmp.h = h
    tmp.o = 'triangle'
    return tmp


class Ellipse(Shape):
    def __init__(self,w,h):
        self.pts=[(0,0)]
        self.w=w
        self.h=h
        self.r=0
        self.fillColor='red'
    def draw(self,dwg):
        e =  dwg.ellipse( center=(self.pts[0][0], self.pts[0][1]), r=(self.w, self.h), fill=self.fillColor ) 
        e.rotate(self.r, (self.pts[0][0], self.pts[0][1]))
        #group.add(e)
        return e
    def rotate(self,_d):
         self.r += _d
         _d = _d * (pi/180)
         self.pts = [ ( (cos(_d) * x - sin(_d) * y),  (sin(_d) * x + cos(_d) * y) ) for x,y in self.pts ]
         return self


## Copy an object into a grid
def make_grid(group, startx, starty, boxSize, count):
    tmp = []
    for x in range(0, count):
        for y in range(0,count):
            tmp_o = copy.deepcopy(group)
            tmp_o.set_name()
            tmp_o.translate( (startx + (x*boxSize))-(G_WIDTH/2) , (starty + (y*boxSize))-(G_HEIGHT/2) )
            tmp.append(tmp_o)
    return Group( *tmp )

r = Renderer(G_WIDTH, G_HEIGHT)

# DG:
# E20,20 T10,0 Fblack RS4,
# E15,15 T10,0 Fwhite RS4;

"""
g = Group(
Group(Ellipse(20,20).translate(10,0).set('fillColor', 'black') ).radial_sym(4),
Group(Ellipse(15,15).translate(10,0).set('fillColor','white') ).radial_sym(4),
Group(Ellipse(8,4).translate(13,0).set('fillColor','black') ).radial_sym(4),
Group(Ellipse(5,5).set('fillColor','red') )
)

gridg = make_grid(g, -200,-200, 60, 20)
r.append( gridg)
t = Group( rect(10, 10).rotate(45).set('fillColor', 'black') )
t = make_grid( t, -200,-200, 30,35)
#r.append(middleGrid)
r.append( t)

"""
r.append( Group(rect(10,10) ) )
r.append( Group(rect(20,20) ) )
# r.append( rect(10,10) )
print(r.root.items())
r.render()
