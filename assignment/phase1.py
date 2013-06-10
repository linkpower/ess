# -*- coding: cp950 -*-
#   test 7

import xml.dom.minidom as minidom
import sys

inputFilePath = ".\\英文街道名.xml"
outputFilePath = ".\\phase1Output.xml"

inputFile = open(inputFilePath, 'r')
outputFile = open(outputFilePath, 'w')

dom = minidom.parse(inputFile)
header = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<Grammars>
<Dictionary name="Place" case="on">
"""
footer = """</Dictionary>
<Grammar name="hk_street">
  	<Entity name="edk_street" type="public">
		<Pattern>(?A:Place/StreetName)</Pattern>
	</Entity>
</Grammar>
</Grammars>
"""
outputFile.write(header)
def readBody(dom):
    body = dom.getElementsByTagName("w:body")[0]
    readTable(body)

def readTable(body):
    parentList = []
    for table in body.getElementsByTagName("w:tbl"):
        area = table.previousSibling
# dont seem to be important
#        if area.previousSibling.tagName == "w:p":
#            district = area.previousSibling
#            printDistrict(district)
        printArea(area)
        printTable(table)
                
def printDistrict(district):
    outputFile.write("    <EntrySet name=\"StreetName\" district=\"")
    for node in district.getElementsByTagName("w:t"):
        printNodeText(node)
    outputFile.write("\">")
    outputFile.write("\n")

def printArea(area):
    outputFile.write("    <EntrySet name=\"StreetName\" district=\"")
    for node in area.getElementsByTagName("w:t"):
        printNodeText(node)
    outputFile.write("\">")
    outputFile.write("\n")

def printTable(table):
    rowList = []
    rowList = table.getElementsByTagName("w:tr")
    for row in rowList:
        columns = row.getElementsByTagName("w:tc")
        for i in range(0,columns.length):
            if i%2 == 0:
                test = columns[i].getElementsByTagName("w:t")
                if test.length == 0:
                    continue
                outputFile.write("      <Entry headword=\"")
                for columnDetail in test:
                    printNodeText(columnDetail)
                outputFile.write("\"/>\n")
            else:
                continue
    outputFile.write("    </EntrySet>\n")

def printNodeText(node):
    outputFile.write("%s" % (getText(node.childNodes)).encode('utf-8','ignore') )

def getText(nodeList):
    rc = ""
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE and node.length > 0:
            rc = rc + node.data
    return rc
    

readBody(dom)
outputFile.write(footer)
