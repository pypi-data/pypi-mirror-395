"""
Script to manipulate the Parameter.in file of ProDiMo.

Currently only on parameter can be changed or appended to an existing file.

This is still experimental stuff ... .

TODO: maybe automatic backup of old file ...
TODO: maybe change of multiple parameters ...
TODO: maybe make some checks (e.g. by finding out the type of the old parameter and
      new value must have the same type)
TODO: make a routine so that it can be use also in other scripts
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import glob
import os

import prodimopy.utils as putils


# the above two statement are for phyton2 pyhton3 compatibility.
# With this statmens you can write python3 code and it should also work
# in python2 (depends on your code)
# this is for the argument parser included in python
# The main routine is require to have an entry point.
# It is not necessary if you want to write your own script.
def main(args=None):
  ###############################################################################
  # Command line parsing
  # this is optional you do not have to do it this way.
  # You can use the prodimopy module in any way you want
  parser=argparse.ArgumentParser(description='Changing of parameters in the ProDiMo Parameter files. The changes can usually not be easily undone, so use with care and make a backup.')
  parser.add_argument('paramname',
                      help='The name of the Parameter in Parameter.in.')
  parser.add_argument('value',
                      help='The value of the parameter to change. If the value==DELETEPARAM, the parameter will be deleted')
  parser.add_argument('-direxp',default=".",
                      help="Change Parameters in all the given model directories. Just pass a regex that is understood by glob.glob. To change all Parameter.in files in the current and all subdirecories use './**'.")
  parser.add_argument('-file',required=False,default="Parameter.in",
                      help='File path to the Parameter file. DEFAULT: Parameter.in')
  args=parser.parse_args()

  print("paramname: ",args.paramname)
  print("value: ",args.value)
  print("-direxp: ",args.direxp)
  print("-file: ",args.file)

  # for this I search
  param="! "+args.paramname.strip()+" "

  # get the directories
  dirs=glob.glob(args.direxp,recursive=True)
  print("")

  for dirname in dirs:
    # Check if files exists, if not just ignore it
    if not os.path.exists(dirname+"/"+args.file): continue
    print("Change Parameter file: "+dirname+"/"+args.file)
    f=open(dirname+"/"+args.file)
    inlines=f.readlines()
    f.close()

    inlines=putils.set_param(inlines,param,args.value)

    f=open(dirname+"/"+args.file,"w")
    f.write("".join(inlines))
    f.close()

