"""
.. module:: postprocessing
   :synopsis: Postprocessing routines for |prodimo|.

.. moduleauthor:: A. M. Arabhavi


"""

from astropy.io import fits
from scipy.constants import atomic_mass as amu
from scipy.constants import c,k,h
from scipy.interpolate import CubicSpline

import numpy as np
import pandas as pd
from prodimopy import hitran as ht
from prodimopy import read_slab as rs
from prodimopy import run_slab as ru
import prodimopy.read as pread


def calculate_population_grid(molecule,iso,T,lvldata,QTpath,HITRAN_QT):
    """
    Calculate the level population grid based on T grid of the 2D disk
    """
    QT=np.zeros_like(T)
    if HITRAN_QT:
        for i in range(T.shape[0]):
            for j in range(T.shape[1]):
                QT[i,j,0]=ru.fetch_QT(molecule,iso,T[i,j,0],QTpath,verbose=False)
    else:
        print('Using user supplied partition sums for ',molecule)
        QT_file_data=np.loadtxt(QTpath)
        QT_file_data=QT_file_data[QT_file_data[:,0].argsort()]
        QT_function=CubicSpline(QT_file_data[:,0],QT_file_data[:,1])
        QT[:,:,:]=QT_function(T)
    pop=ru.boltzmann_distribution(lvldata[:,:,:,0],lvldata[:,:,:,1],T,QT)
    return pop


def postprocess_lines(QTpath='.',directory='.',linemode='replace',input_file='ProDiMoForFLiTs.fits.gz',output_file='ProDiMoForFLiTs_PP.fits.gz',lineselection='LineSelectionPP.in'):
    """
    Edit ProDiMoForFLiTs.fits.gz function to add new lines and species

    Parameters
    ----------

    QTpath : string
      Path to the QTpy folder downloaded from HITRAN

    directory : string
      Working directory that contains |prodimo| outputs and the fits file. The output also uses this parent directory.

    linemode : str
      Can be 'replace' or 'add'
      'replace' will replace existing occrence, if any, of the species in the .fits file. If not present, then it will automatically add new HDU.
      'add' will add another HDU with the species, irrespective of whether it already exists.

    input_file : str
      Filename of existing .fits file that is to be modified

    output_file : str
      Output file name, should end with '.fits'

    lineselection : string
      Path to file which specifies the line selection

    """
    if not (linemode in ['replace','add']): raise ValueError('linemode only takes in "replace" or "add"')
    model=pread.read_prodimo(directory,readlineEstimates=False,readObs=False,readImages=False)
    if input_file==output_file:
        mode='update'
    else:
        mode='readonly'
    with fits.open(directory+'/'+input_file,mode=mode) as forflits:
        numdens=forflits[11].data
        rules=ht.read_line_selection(directory+'/'+lineselection)
        spindex=np.zeros((len(rules)),dtype=int)
        sp=pd.DataFrame()
        sp['ind']=[]
        sp['species']=[]
        for i,j in enumerate(model.spnames):
            sp.loc[len(sp.index)]=[i,j]
        for i in range(len(rules)):
            if rules[i].prodimo_name is None: rules[i].prodimo_name=rules[i].name
            location=sp.index[sp['species']==rules[i].prodimo_name.split('_')[0]]
            if len(location)<=0:
                raise ValueError(f'{rules[i].name} is not found in ProDiMo.out!')
            else:
                spindex[i]=location[0]

        T=forflits[1].data.reshape((forflits[1].data.shape[0],forflits[1].data.shape[1],1))
        mol_list=pd.DataFrame()
        mol_list['ind']=[]
        mol_list['species']=[]

        for i in range(forflits[0].header['NSPEC']):
            mol_list.loc[len(mol_list.index)]=[i+13,forflits[i+13].header['SPECIES']]

        for i,rule in enumerate(rules):
            dat=ht.read_hitran_from_rules(rule)
            dattt,datttt=ht.create_lamda_line_level(dat)
            if rule.output_file is None:
                print(f'WARNING: no LAMDA output file name given, using {rule.name}_Lambda_PP.dat instead!!')
                lambda_output_file=directory+f'/{rule.name}_Lambda_PP.dat'
            else:
                lambda_output_file=directory+'/'+rule.output_file
            ht.write_lamda_file(dattt,datttt,rule.name,rule.mass,lambda_output_file)
            if (rule.custom_partition_sum is None):
                pop=calculate_population_grid(rule.name.split('_')[0],rule.iso,T,datttt,QTpath=QTpath,HITRAN_QT=True)
            else:
                pop=calculate_population_grid(rule.name.split('_')[0],rule.iso,T,datttt,QTpath=rule.custom_partition_sum,HITRAN_QT=False)
            location=mol_list.index[mol_list['species']==rule.name]
            if linemode=='replace' and len(location)>0:
                forflits[mol_list['ind'][location[0]]].header['NLEV']=pop.shape[-1]
                forflits[mol_list['ind'][location[0]]].header['NAXIS1']=pop.shape[-1]
                forflits[mol_list['ind'][location[0]]].data=pop
                # Change number density by rule.abundance_fraction
            else:
                newhdu=fits.ImageHDU(pop)
                newhdu.header['NLEV']=pop.shape[-1]
                newhdu.header['SPECIES']=rule.name
                forflits.append(newhdu)
                forflits[0].header['NSPEC']+=1
                forflits[11].header['NAXIS1']=forflits[0].header['NSPEC']
                numdens=np.append(numdens,model.nmol[:,:,spindex[i]].T.reshape(model.nmol.shape[1],model.nmol.shape[0],1)*rule.abundance_fraction,axis=2)
                forflits[11].data=numdens
                numdens=forflits[11].data
 # TO DO          # Change this to read in the turbulent velocity structure of ProDiMo model.
                vtot=forflits[12].data
                vth=(2*k*forflits[1].data/(rule.mass*amu))**0.5*1e2
                v=((model.p_v_turb*1e5)**2+(vth)**2)**0.5
                vtot=np.append(vtot,v.reshape(vtot.shape[0],vtot.shape[1],1),axis=2)
                forflits[12].data=vtot
                forflits[12].header['NAXIS1']=forflits[0].header['NSPEC']
        if mode=='update':
            print(f"Writing output to {directory+'/'+output_file}")
            print('Rewriting the file might sometimes not work, suggest using different output file name')
            # NOT WORKING, FIX ME!!

            forflits.flush()  # writeto(directory+'/ProDiMoForFLiTs.fits.gz',overwrite=True)
        else:
            print(f"Writing output to {directory+'/'+output_file}")
            forflits.writeto(directory+'/'+output_file,overwrite=True)
    forflits.close()
    return

