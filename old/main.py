#!/usr/bin/env python

# https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/tiling_part_1.py

from pattern import *

"""
def create_svg(name):
    svg_size_width = 800
    svg_size_height = 800
    font_size = 20
    square_size = 80
    dwg = svgwrite.Drawing(name, debug=True, size=("10cm", "10cm"))
    dwg.viewbox(0, 0, 80, 80)

    shapes = dwg.add( dwg.g(id='shapes', fill='red') )
  
    rw=20
    for r in range(0,360,45):
        rec = dwg.rect(insert=( (square_size/2)-(rw/2) ,0), size=(rw,rw))
        rec.rotate(angle=r,center=(40,40) ) 
        shapes.add( rec)
        #shapes.rotate(angle=r,center=(40,40) ) 

    dwg.save()

    
if __name__ == '__main__':
    create_svg("test.svg")
"""

size( (100,100), (80,80) )
unit("cm")
name("test.svg")

for i in range(0,360,15):
    r = rect(0,0, 10,10)
    r.rotate(i)
    r.translate(0,30)
    add( r)

save()
