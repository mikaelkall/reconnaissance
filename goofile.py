#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
   goofile.py

   Quick rewrite of goofile for reconnaissance 
   as old implementation seems to be broken.  

"""
__author__ = 'kall.micke@gmail.com'

import requests
import sys
import os
import re
import getopt
import string

def search(dmn, file):

   session = requests.session()
   session.headers.update({'User-Agent': 'Mozilla/5.0'})

   url = 'https://www.google.se/search?source=hp&ei=Cl5TWpf-B4ucgAa2garQDw&q=inurl%3A'+ dmn +'+ext%3A'+ file + '&oq=inurl%3A'+ dmn +'+ext%3A' + file \
           + 'f&gs_l=psy-ab.3...55500.109023.0.109123.50.30.3.0.0.0.0.0..0.0....0...1c.1.64.psy-ab..47.3.29...0j0i131k1.0.e-jqjT2O8DY' 
   r = session.get(url)

   for e in ('>','=','<','\\','(',')','"','http',':','//'):
      data = string.replace(r.text,e,' ')
   r1 = re.compile('[-_.a-zA-Z0-9.-_]*'+'\.'+ file)
   res = r1.findall(data)

   url = [url for url in res if bool(re.match(r'^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}.*', url.strip()))]
   # Remove duplicates
   url = list(set(url))

   for u in url:
      print("https://%s" % u)


def __usage():
   print ("""   
[Goofile] 

usage: goofile <options>
       -d: domain to search
       -f: filetype (ex, pdf)     

example: ./goofile.py -d test.com -f txt
""")
   sys.exit()


if __name__ == "__main__":

        if len(sys.argv) < 2:
                __usage()
        try :
              opts, args = getopt.getopt(sys.argv[1:],"d:f:")

        except getopt.GetoptError:
                __usage()
                sys.exit()

        for opt,arg in opts :
            if opt == '-f' :
               file=arg
            elif opt == '-d':
                dmn=arg

        print("Searching in %s for %s\n" % (dmn, file))
        search(dmn, file)
