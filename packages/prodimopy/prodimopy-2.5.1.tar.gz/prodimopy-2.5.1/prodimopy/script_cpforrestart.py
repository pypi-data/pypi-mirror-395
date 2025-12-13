'''
  Simple script to copy an existing model to a new directory and prepare if for restart.

  The script only copies required files, not the output (results) files. 
  
  Type pcpforrestart.py -h for help.

  ..todo::

    - make the routine modular (e.g. to use it in another python script)

'''
import argparse
import os
import glob
import prodimopy.utils as putils

import shutil
import json


# The main routine is require to have an entry point.
# It is not necessary if you want to write your own script.
def main(args=None):
  parser=argparse.ArgumentParser(description='Compares two ProDiMo models')
  parser.add_argument('srcDir',help='The directory from where we want to copy the model. Just use . for current directory')
  parser.add_argument('destDir',help='The directory for the new model. It is a relative path. The new model will be at the same directory level as the old model.')
  parser.add_argument('-tdIdx',
                      help="The time-dependent file index (e.g. the postfix for restart.fits.gz) of the source dir. "
                      "The files corresponding to this index (timestamp) are copied for restart. Only the number is required, and it starts with 1",
                      default=None)
  parser.add_argument('-pr', action='store_false',help='Set the restart parameter to true in the Parameter.in.',default=True)
  parser.add_argument('-pfrt', action='store_true',help='Set the freeze_RT parameter to true in the Parameter.in.',default=False)
  parser.add_argument('-pftgas', action='store_true',help='Set the freeze_Tgas parameter to true in the Parameter.in.',default=False)
  parser.add_argument('-pfchem', action='store_true',help='Set the freeze_chemistry parameter to true in the Parameter.in.',default=False)
  parser.add_argument('-pfstruc', action='store_true',help='Set the freeze_diskstruc parameter to true in the Parameter.in.',default=False)
  parser.add_argument('-pdict', help='Dictionary with parameter names and values that should also be set.',default="{}")

#  parser.add_argument('overwrite',help='Overwrite destDir if it already exists.',default=False)
  args=parser.parse_args()

  addparams=json.loads(args.pdict)

  if args.srcDir==".": args.destDir=os.path.join("..",args.destDir)

  print("Copy model "+args.srcDir+" to "+args.destDir)

  if os.path.isdir(args.destDir):
    print("ERROR: Destination directory already exists. Please delete or choose another directory.")
    return
  
  # Create the directory
  os.mkdir(args.destDir)
  
  # now copy the files we want
  for fname in glob.glob(os.path.join(args.srcDir,"*.in")):
    print("Copying "+fname +" to "+ args.destDir)
    shutil.copy2(fname,args.destDir)

  # also copy all dat files, those should contain observational data
  for fname in glob.glob(os.path.join(args.srcDir,"*.dat")):
    # exclude the eventually produced _Lambda.dat filed
    if not fname.endswith("_Lambda.dat"):    
      print("Copying "+fname +" to "+ args.destDir)
      shutil.copy2(fname,args.destDir)

  restartfilename="restart.fits.gz"
  if args.tdIdx!=None:
    # In the newest version it is four digits ... try also older ones
    for width in ["04","03","02"]:
      postfix="{0:{width}d}".format(int(args.tdIdx),width=width)
      restartfilename="restart_"+postfix+".fits.gz"
      # if it is there we are done
      if (os.path.isfile(os.path.join(args.srcDir,restartfilename))):
        break

  # Copy the Mie.fits.gz and the restart.fits.gz
  for file in [restartfilename,"Mie.fits.gz"]:
    fname=os.path.join(args.srcDir,file)
    print("Copying "+fname +" to "+ args.destDir)
    shutil.copy2(fname,args.destDir)

  # manipulate the parameter file
  print(" ")
  print("Manipulating "+os.path.join(args.destDir,"Parameter.in")+" ...")
  f=open(os.path.join(args.destDir,"Parameter.in"))
  inlines=f.readlines()
  f.close()

  if args.pr:
    inlines=putils.set_param(inlines,"! restart",".true.")
  if args.pfrt:
    inlines=putils.set_param(inlines,"! freeze_RT",".true.")
  if args.pftgas:
    inlines=putils.set_param(inlines,"! freeze_Tgas",".true.")
  if args.pfchem:
    inlines=putils.set_param(inlines,"! freeze_chemistry",".true.")

  for key, value in addparams.items():
    if key[0]!="!":
      key="! "+key
    key=key.strip()+" "
    inlines=putils.set_param(inlines,key,value)

  f=open(os.path.join(args.destDir,"Parameter.in"),"w")
  f.write("".join(inlines))
  f.close()
  