from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from astropy import units as u


def calc_dustcolumnd(model):
  '''
  Calculated the vertical column density for every species at every point
  in the disk (from top to bottom). Very simple and rough method.

  :param model: the |prodimo| model
  :return cd: mass column density for the dust at every point

  TODO: maye put this back into the data structure as util function or both=
  '''
  cd=0.0*model.rhod
  for ix in range(model.nx):
    for iz in range(model.nz-2,-1,-1):  # from top to bottom
      dz=(model.z[ix,iz+1]-model.z[ix,iz])
      dz=dz*u.au.to(u.cm)
      nn=0.5*(model.rhod[ix,iz+1]+model.rhod[ix,iz])
      cd[ix,iz]=cd[ix,iz+1]+nn*dz

  return cd


def load_mplstyle(stylename="prodimopy"):
  '''
  Simple utility function to load a matplotlib style.  

  In case of `stylename=="prodimopy"` it will load the mplstyle file from 
  within the prodimopy package. 

  Parameters
  ----------

  style : str
    The name of the style that should be loaded. Default: `prodimopy`

  '''
  import matplotlib.pyplot as plt
  if stylename=="prodimopy":
    plt.style.use("prodimopy.stylelib.prodimopy")
    print("INFO: Load "+stylename+" mplstyle from package.")
  elif stylename=="notebook" or stylename=="nb":
    plt.style.use(["prodimopy.stylelib.prodimopy","prodimopy.stylelib.prodimopy_nb"])
    print("INFO: Load prodimopy"+stylename+" mplstyle from package.")
  else:
    styles=plt.style.available
    if stylename in styles:
      plt.style.use(stylename)
      print("INFO: Load "+stylename+" mplstyle.")
    else:
      print("WARN: Could not load "+stylename+" mplstyle.")


def set_param(paramFileList,param,value):
  """
  Utility function that allows to change |prodimo| parameter values in a list
  of |prodimo| Parameters (e.g. read in from Parameter.in)

  If the parameter is not found in the file it will append it at the end of the
  file.

  If `value==DELETEPARAM` the routine will delete he line containing that parameter.

  This routine cannot deal yet with complex parameter structures. Only works
  with parameters that have a single value.

  Parameters
  ----------
  paramFileList : list()
    The content of the Parameter.in as a list.
    You can get it via `f.readLines()`
    This can also be a list that already includes changed parameters.
    Each entry in the list should correspond to one Parameter.
    Please note this input will be changed directly (i.e. the list is not copied).

  param : str
    The |prodimo| parameter name (including the ! )

  value : str
    the parameter value. The string will be used as is.
    If value is `"DELETEPARAM"` the parameter will be deleted.
    There are no checks or anything.


  Returns
  -------
  list
    the paramFileList

  _todo: This is quick and dirty ... maybe it is worth to make this more elegant and more flexible (e.g. its own class, allow to set comments etc.)

  """

  # figure out if we can skip the line from the Parameter file
  skipline=lambda pline: pline.strip()=="" or pline.strip().startswith("***") or pline.strip().startswith("---")
  # find the Parameter in line from he Parameter file
  findparam=lambda pline,param: (pline.strip()+" ").find(param)

  # add a space to param
  param=param.strip()+" "

  # delete the parameter
  if value.strip()=="DELETEPARAM":
    for i in range(len(paramFileList)):
      if skipline(paramFileList[i]): continue
      if findparam(paramFileList[i],param)>-1:
        print("delete line : "+paramFileList[i])
        paramFileList.pop(i)
        return paramFileList
    print("Parameter '"+param+"' not found.")
    return paramFileList

  replaced=False
  for i in range(len(paramFileList)):
    if skipline(paramFileList[i]): continue
    ip=findparam(paramFileList[i],param)
    if ip>-1:
      val=paramFileList[i][0:ip-1]
      rest=paramFileList[i][ip:]
      lval=len(val)
      lnewval=len(value)
      if lval>lnewval:
        newval=value+" "*(lval-lnewval)+" "
      elif lval<lnewval:
        newval=value+"  "
      else:
        newval=value+" "
      # print(val,rest,lval,lnewval,newval)

      paramFileList[i]=newval+rest
      print("change : ",paramFileList[i])
      replaced=True

  if not replaced:
    paramFileList.append(value+"  "+param+"\n")
    print("append : ",paramFileList[-1])

  return paramFileList
