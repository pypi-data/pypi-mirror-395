"""
Simple script to run prodimo from the command line.

Mainly for convenience. The script makes sure that the log output is written to a file, but also allows to e.g. set the number of threads.
"""

import argparse

import shutil
import subprocess
import os
import resource
from timeit import default_timer as timer
from datetime import timedelta
import sys


# The main routine is require to have an entry point.
# It is not necessary if you want to write your own script.
def main(args=None):
    parser = argparse.ArgumentParser(description="Runs ProDiMo in the current working directory.")
    parser.add_argument(
        "PARAMA",
        nargs="?",
        help="Add additional Parameter input file (additional to Parameter.in)",
        default=None,
    )
    parser.add_argument(
        "-n",
        help="The number of OMP threads to use. (Default is System settings, e.g. what's in OMP_NUM_THREADS)",
        default=None,
    )
    parser.add_argument(
        "-all",
        action="store_true",
        help="Try to run all models in the current directory (so all subdirectories)",
        default=None,
    )
    parser.add_argument(
        "-wait",
        action="store_true",
        help="Wait for the ProDiMo process to finish (i.e. do not launch in the background). In that case also information about runtime and memory usage is provided.",
        default=None,
    )
    parser.add_argument(
        "-notime",
        action="store_true",
        help="Don't use time command to measuere resource usage.",
        default=None,
    )

    args = parser.parse_args()

    # Check if prodimo is in the path
    prodimopath = shutil.which("prodimo")
    if prodimopath is None:
        print(
            "ERROR: prodimo is not in the path. Please add it to the path, or provide the path to the executable."
        )
        return

    # check for macOSX
    macosx = sys.platform=="darwin"

    # check for special time command, on linux there might be gnu time on mac something else
    timecmd = shutil.which("/usr/bin/time")
    if timecmd is not None and args.notime is None:
        # on Mac os x there seems to be something like bsd time 
        if macosx:
            callargs = [timecmd, "-l"]
        else:
            callargs = [timecmd, "-v"]
        callargs.append( prodimopath )    
    else:
        timecmd=None
        callargs = [prodimopath]

    if args.PARAMA is not None:
        callargs.append(args.PARAMA)

    print("Run ProDiMo with: ", " ".join(callargs), " ...")

    penv = os.environ.copy()
    if args.n is not None:
        print("Setting number of OMP threads to: ", args.n)
        penv = os.environ.copy()
        penv["OMP_NUM_THREADS"] = args.n.strip()

    modeldirs = []
    if args.all is not None:
        for dir in os.listdir("."):
            if os.path.isdir(dir):
                modeldirs.append(dir)
        if args.wait is not None:
            print("Try to run ", len(modeldirs), " models one after the other ...")
        else:
            print("Try to run ", len(modeldirs), " models in parallel ...")
        print("")
    else:
        modeldirs.append(".")

    for modeldir in modeldirs:
        print("Running model in directory: ", modeldir)

        if not os.path.isfile(os.path.join(modeldir, "Parameter.in")):
            print("  Skipping directory ", modeldir, " as no Parameter.in file was found.")
            continue
        os.chdir(modeldir)

        print("You can check the progress by looking at the file prodimo.log")
        
        # So this is just for a single run, with wait, to get resource usage.
        if args.wait and len(modeldirs)==1 and timecmd is None:     
            toGB = 1024**2  # on Linux it seems to be in kB            
            if macosx:
                toGB = 1024**3  # on macOS it seems to be in bytes        
       
            with open("prodimo.log", "w") as f:
                start_time = timer()
                proc = subprocess.run(callargs, stdout=f, stderr=f, env=penv)
                runtime = timer()-start_time            
                res = resource.getrusage(resource.RUSAGE_CHILDREN)
            # This stuff only works for single runs
            print("Real time: ", f"{timedelta(seconds=runtime)}")
            print("User time: ", f"{timedelta(seconds=res.ru_utime)}")                            
            print(f"Max memory used: {res.ru_maxrss/toGB:8.3f} GB")

            print("ProDiMo finished. You can check the output in ",os.path.join(modeldir,"prodimo.log"))
            print()
        elif args.wait: # if timecmd is used it will provide resource usages in the logfile
            with open("prodimo.log", "w") as f:
                proc = subprocess.run(callargs, stdout=f, stderr=f, env=penv)
        else: # also here it should work
            with open("prodimo.log", "w") as f:
                proc = subprocess.Popen(callargs, stdout=f, stderr=f, env=penv)

            print("You can stop ProDiMo by killing the process with:  kill ", proc.pid)

        if modeldir != ".":
            os.chdir("..")

        print()

    # subprocess.run(executable=prodimopath,args=[">","prodimo.log"],STD)
