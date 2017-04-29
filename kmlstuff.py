# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pykml import parser
from lxml import etree
from io import StringIO, BytesIO
f = open('VNP14IMGTDL_NRT_Australia_and_New_Zealand_24h.kml','r')
marks = parser.parse(f)
f.close()
marks.getroot()
doc = marks.getroot()
doc2 = etree.tostring(marks)
marks2 = parser.fromstring(doc2)

str(marks2.Document.Folder.Placemark.description)[58+16:58+26]

a = marks2.getroottree()
f = open('newkml.kml','w')
f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
a.write(f)
f.close()


#for mark in marks.iter():
#    print mark
#    
#f = open('test.kml','w')
#f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
#marks.write(f)
#f.close()

#from pykml.factory import write_python_script_for_kml_document
#
#script = write_python_script_for_kml_document(doc)
#f = open('newkml.py','w')
#f.write(script)
#f.close()
#
#execfile('newkml.py')