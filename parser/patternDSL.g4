// varname = ( drawing objects) (group options)
// group1 = ( R10,10 T60,0 C"red" | R20,20 T-60,0 C"blue" | E10,10 T90,0) (rot45 rt5)
// RENDER( group1, group2, group3)

grammar patternDSL;

start:  pgrm+ ;

pgrm
    : render 
    | group
    | grid
    ;

group: VARNAME EQ RP groupdef (COMMA groupdef)* LP EOC;

groupdef: RP shpcmd shpopts* ('|' shpcmd shpopts*)* LP RP grpcmd* LP;

grid: VARNAME EQ 'GRID' INT COMMA INT COMMA INT COMMA VARNAME EOC;

render: 'RENDER' RP VARNAME (',' VARNAME)* LP EOC;

shpcmd 
       : ('R'|'RECT') INT COMMA INT  # rect 
       | ('E'|'ELLIPSE') INT COMMA INT # ellipse 
       ;   

shpopts
      : ('T'|'TRANSLATE') INT COMMA INT # shapetranslate
      | ('C'|'COLOR') INT   # shapesetcolor
      | ('RT'|'ROTATE') INT # shaperotate
      ;

grpcmd
      : ('RT' | 'ROTATE') INT  #grouprotate
      | ('RS' | 'RADIALSYM') INT #groupradialsym 
      ;

COMMA: ',';
EOC: ';';
EQ: '=';
RP: '(';
LP: ')';
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
INT: [0-9]+;
VARNAME: [a-zA-Z][a-zA-Z]+;
