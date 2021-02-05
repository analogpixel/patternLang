bin=./pattern.py
gapplin=/Applications/Gapplin.app/Contents/MacOS/Gapplin
antlr=java -jar /usr/local/lib/antlr-4.9-complete.jar

buildParser: parser/patternDSL.g4
	$(antlr) -Dlanguage=Python2 parser/patternDSL.g4

svg:
	$(bin)

open:
	$(gapplin) 

all: buildParser
