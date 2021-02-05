#!/usr/bin/env python

from pattern import *
from antlr4 import *
from parser.patternDSLLexer import patternDSLLexer
from parser.patternDSLListener import patternDSLListener
from parser.patternDSLParser import patternDSLParser
import sys

G_WIDTH = 800
G_HEIGHT = 800

"""
r = Renderer(G_WIDTH, G_HEIGHT)

# DG:
# E20,20 T10,0 Fblack RS4,
# E15,15 T10,0 Fwhite RS4;

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
r.append( t)

r.render()
"""

class createPatterns(patternDSLListener):

    def __init__(self):
        self.render = Renderer(G_WIDTH, G_HEIGHT)
        self.parentGroup = False
        self.groupData = {}
        self.groupItems = []
        self.currentGroup = False
        self.currentGroupName = False
        self.colors = ['black', 'white', 'red','blue','green','yellow']
        self.RS = False

    def enterRect(self,ctx):
        x = int(ctx.getChild(1).getText() )
        y = int(ctx.getChild(3).getText() )
        print("Rect:", x,y)
        self.groupItems.append( rect(x,y) )

    def enterShapetranslate(self,ctx):
        x = int(ctx.getChild(1).getText() )
        y = int(ctx.getChild(3).getText() )
        self.groupItems[-1].translate(x,y)

    def enterEllipse(self,ctx):
        x = int(ctx.getChild(1).getText() )
        y = int(ctx.getChild(3).getText() )
        self.groupItems.append( Ellipse(x,y) )
        print("ellipse:", x,y)

    def enterGroup(self, ctx):
        print("Enter a new group")
        self.parentGroup = Group()
        self.currentGroupName = ctx.VARNAME().getText() 

    def enterGroupdef(self,ctx):
        self.currentGroup = Group()
        self.groupItems = []

    def enterShapesetcolor(self,ctx):
        c = int(ctx.getChild(1).getText() )
        self.groupItems[-1].set('fillColor', self.colors[c])
        print("set color to:", c)

    def enterShaperotate(self,ctx):
        r = int(ctx.getChild(1).getText() )
        self.groupItems[-1].rotate(r)
        print("rotate:", r)

    def exitGrouprotate(self,ctx):
        r = int(ctx.getChild(1).getText() )
        self.currentGroup.rotate(r)
        print("rotate group:", r)
    
    def enterGroupradialsym(self,ctx):
        r = int(ctx.getChild(1).getText() )
        self.RS = r
        print("radial sym group:", r)

    def exitGroupdef(self, ctx):
        print("Adding Items to new group")
        for g in self.groupItems:
            self.currentGroup.append(g)
        
        # since this copies objects, objects need to be in the group
        # before we do this
        if self.RS:
            self.currentGroup.radial_sym(self.RS)

        self.parentGroup.append( copy.deepcopy(self.currentGroup))
        self.groupItems = []

    def exitGroup(self,ctx):
        self.groupData[self.currentGroupName] = copy.deepcopy(self.parentGroup)

    def enterPgrm(self,ctx):
        print("Enter pgrm", ctx.getText() )

    def exitGrid(self,ctx):
        gridVar = ctx.getChild(0).getText() 
        fromVar = ctx.getChild(9).getText()

        print("create grid for var:", gridVar, " from var:", fromVar)
        self.groupData[gridVar] = make_grid( self.groupData[fromVar], -200,200, 60,20)
    
    # used to add objects to the renderer
    def exitRender(self,ctx):
        for obj in ctx.VARNAME():
            self.render.append( self.groupData[obj.getText()] )
            print("Add group to renderer:", obj.getText() )

    def exitStart(self,ctx):
        print("ok render it")
        self.render.render()

test1="bob = (E20,20 T90,0 RT45 C0)(RS10); RENDER(bob);"

test2="""
ga = ((E20,20 T10,0 C0 )(RS4), (E15,15 T10,0 C1 )(RS4), (E8,4 T13,0 C0)(RS4));
mrgrid = GRID10,10,20,ga;
RENDER(mrgrid);
"""

def main():
    lexer = patternDSLLexer(InputStream(test2))
    stream = CommonTokenStream(lexer)
    parser = patternDSLParser(stream)

    tree = parser.start()

    printer = createPatterns()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main()

