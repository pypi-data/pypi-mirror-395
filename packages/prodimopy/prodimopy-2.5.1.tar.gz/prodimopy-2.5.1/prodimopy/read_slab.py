"""
.. module:: read_slab
   :synopsis: Read routines and data structure for prodimo slab models.

.. moduleauthor:: A. M. Arabhavi


"""

import os
import string

from astropy.convolution import Gaussian1DKernel
from astropy.convolution import convolve as apy_convolve
from astropy.io import fits
from scipy.constants import astronomical_unit as au
from scipy.constants import h,c,k
from scipy.constants import parsec as pc
from scipy.special import erf as serf
try:
    from spectres import spectres_numba as spectres
except: 
    from spectres import spectres

import numpy as np
import pandas as pd

kmps = 1e3

class MyFormatter(string.Formatter):
    """
    String formatter for producing input files
    """

    def format_field(self,value,format_spec):
        if format_spec[-1]=='m':
            return super().format_field(value,format_spec[:-1]+'e').replace('e+','e')
        else:
            return super().format_field(value,format_spec)


fmt=MyFormatter()

class slab_data:
    """
    Structure of the models set up from the SlabInput.in file:

    |prodimo| run

    .. code ::

        |__Model_1
            |__molecule_1
            |__molecule_2
            |__...
            |__molecule_n
        |__Model_2
            |__molecule_1
            |__molecule_2
            |__...
            |__molecule_n
        |__...
            |__...

            |__...

            |__...
        |__Model_n
            |__molecule_1
            |__molecule_2
            |__...
            |__molecule_n


    Data structure to hold the corresponding slab model output
    slab_data


    .. code::

        |_directory

        |_models
            |__model_1 (type:slab)
                |__prodimo_Model_1_molecule_1
            |__model_2 (type:slab)
                |__prodimo_Model_1_molecule_2
            |__model_... (type:slab)
                |__...
            |__model_n (type:slab)
                |__prodimo_Model_2_molecule_n
            |__model_n+1 (type:slab)
                |__prodimo_Model_2_molecule_1
            |__model_n+2 (type:slab)
                |__prodimo_Model_2_molecule_2
            |__model_... (type:slab)
                |__...
            |__model_n+n (type:slab)
                |__prodimo_Model_2_molecule_n
            |__model_... (type:slab)
                |__...


    """

    def __init__(self):
        self._nmodels=0
        """ integer :
        number of models.
        """

        self.directory=None
        """ string :
        The directory from which the model was read.
        Can be a relative path.
        """
        self.models=[]
        """ list :
        The list containing the models
        """

        self._species_number=None
        """ list:
        It stores the species number according to SlabInput.in of all models
        """

        self._model_number=None
        """ list:
        It stores the model number according to SlabInput.in of all models
        """

        self._NH=None
        """ list:
        It stores the total gas densities of all models
        """

        self._nColl=None
        """ list:
        It stores the total collision partner abundance of all models
        """

        self._ne=None
        """ list:
        It stores the electron abundance of all models
        """

        self._nHe=None
        """ list:
        It stores the He abundance of all models
        """

        self._nHII=None
        """ list:
        It stores the HII abundance of all models
        """

        self._nHI=None
        """ list:
        It stores the HI abundance of all models
        """

        self._nH2=None
        """ list:
        It stores the molecular hydrogen abundance of all models
        """

        self._dust_to_gas=None
        """ list:
        It stores the dust to gas ratio of all models
        """

        self._vturb=None
        """ list:
        It stores the turbulent broadening of all models
        """

        self._Tg=None
        """ list:
        It stores the gas temperatures of all models
        """

        self._Td=None
        """ list:
        It stores the dust temperatures of all models
        """

        self._species_name=None
        """ list:
        It stores the name of the molecules of all models
        """

        self._species_index=None
        """ list:
        It stores the |prodimo| species index of all models
        """

        self._abundance=None
        """ list:
        It stores the species abundance according to SlabInput.in of all models
        """

        self._dv=None
        """ list:
        It stores the velocity width of all models
        """

        self._nlevels=None
        """ list:
        It stores the number of levels of all models
        """

        self._nlines=None
        """ list:
        It stores the number of lines of all models
        """
        self._linedata=None
        """ list:
        It stores the line data of all models
        """

        self._leveldata=None
        """ list:
        It stores the level data of all models
        """

        self._convWavelength=None
        """ list:
        It stores the convolved wavelength grid of all models
        """

        self._convLTEflux=None
        """ list:
        It stores the convolved LTE flux of all models
        """

        self._convNLTEflux=None
        """ list:
        It stores the convolved NLTE flux of all models
        """

        self._convType=None
        """ list:
        It stores the convolution type of all models
        """

        self._convR=None
        """ list:
        It stores the convolved resolving power R of all models
        """

        self._convOverlapFreq=None
        """ list:
        It stores the convolved frequency grid of all line overlap models
        """

        self._convOverlapWav=None
        """ list:
        It stores the convolved wavelength grid of all line overlap models
        """

        self._convOverlapLTEflux=None
        """ list:
        It stores the convolved LTE flux of all line overlap models
        """

        self._convOverlapNLTEflux=None
        """ list:
        It stores the convolved NLTE flux of all line overlap models
        """

        self._overlapFreq=None
        """ list:
        It stores the frequency grid of all line overlap models
        """

        self._overlapLTE=None
        """ list:
        It stores the convolved LTE flux of all line overlap models
        """

        self._overlapNLTE=None
        """ list:
        It stores the convolved NLTE flux of all line overlap models
        """

        self._overlapTauLTE=None
        """ list:
        It stores the convolved LTE optical depths of all line overlap models
        """

        self._overlapTauNLTE=None
        """ list:
        It stores the convolved NLTE optical depths of all line overlap models
        """

        self._overlapR=None
        """ list:
        It stores the resolving power R of all line overlap models
        """

        self._convOverlapR=None
        """ list:
        It stores the convolved resolving power R of all line overlap models
        """

    def __str__(self):
        output="Info: \n"
        output+="\n NModels: "
        output+=str(self.nmodels)
        if isinstance(self.directory,list):
            for i in self.directory:
                output+="\n\n Directory: "+i
        else:
            output+="\n\n Directory: "+self.directory
        return output

    def show(self):
        print(self)
        for i in range(self.nmodels):
            self.models[i].show()
            print('\n')

    def add_model(self,model_data):
        if not isinstance(model_data,slab):
            raise TypeError('path must be of class:model')
        self.models.append(model_data)

    def remove_model(self,index):
        if index<0:
            index+=self.nmodels
        if index+1>self.nmodels or index<0:
            raise IndexError('Index out of range')
        else:
            self.nmodels-=1
            self.models.pop(index)

    def __getitem__(self,arg):
        ret_data=slab_data()
        if isinstance(arg,int):
            if arg>self.nmodels:
                raise ValueError(f'index {arg} greater than number of models {self.nmodels}')
            ret_data.add_model(self.models[arg])
        elif isinstance(arg,type(None)):
            for model in self.models:
                ret_data.add_model(model)
        elif isinstance(arg,slice):
            if isinstance(arg.start,int):
                if isinstance(arg.stop,int):
                    for model in self.models[arg]:
                        ret_data.add_model(model)
                elif isinstance(arg.stop,type(None)):
                    ret_data.add_model(self.models[arg.start])
                else:
                    raise IndexError(f'slicing not understandable {arg}')
            elif isinstance(arg.start,str):
                if arg.start=='species_name':
                    sel_species=[]
                    if isinstance(arg.stop,str):
                        sel_species.append(arg.stop)
                    elif isinstance(arg.stop,list):
                        sel_species=arg.stop
                    if len(sel_species)>0:
                        for i in range(self.nmodels):
                            if self.models[i].species_name in sel_species:
                                ret_data.add_model(self.models[i])
                elif arg.start=='species_number':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            for i in range(arg.stop,arg.step):
                                sel_species_number.append(i)
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].species_number in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='model_number':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            for i in range(arg.stop,arg.step):
                                sel_species_number.append(i)
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].model_number in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='NH':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].NH<upper and self.models[i].NH>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].NH==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].NH in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nColl':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].nColl<upper and self.models[i].nColl>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].nColl==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].nColl in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='ne':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].ne<upper and self.models[i].ne>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].ne==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):

                        for i in range(self.nmodels):
                            if self.models[i].ne in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nHe':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].nHe<upper and self.models[i].nHe>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].nHe==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):

                        for i in range(self.nmodels):
                            if self.models[i].nHe in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nHII':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].nHII<upper and self.models[i].nHII>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].nHII==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].nHII in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nHI':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].nHI<upper and self.models[i].nHI>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].nHI==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].nHI in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nH2':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].nH2<upper and self.models[i].nH2>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].nH2==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):

                        for i in range(self.nmodels):
                            if self.models[i].nH2 in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='dust_to_gas':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].dust_to_gas<upper and self.models[i].dust_to_gas>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].dust_to_gas==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):

                        for i in range(self.nmodels):
                            if self.models[i].dust_to_gas in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='vturb':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].vturb<upper and self.models[i].vturb>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].vturb==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].vturb in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='Tg':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].Tg<upper and self.models[i].Tg>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].Tg==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].Tg in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='Td':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].Td<upper and self.models[i].Td>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].Td==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].Td in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='species_index':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            for i in range(arg.stop,arg.step):
                                sel_species_number.append(i)
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].species_index in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='abundance':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].abundance<upper and self.models[i].abundance>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].abundance==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].abundance in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='dv':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].dv<upper and self.models[i].dv>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].dv==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].dv in arg.stop:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nlevels':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            for i in range(arg.stop,arg.step):
                                sel_species_number.append(i)
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].nlevels in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='nlines':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            for i in range(arg.stop,arg.step):
                                sel_species_number.append(i)
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].nlines in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='convType':
                    sel_species_number=[]
                    if isinstance(arg.stop,int):
                        if isinstance(arg.step,int):
                            sel_species_number=[arg.stop,arg.step]
                        else:
                            sel_species_number.append(arg.stop)
                    elif isinstance(arg.stop,list):
                            sel_species_number=arg.stop
                    if len(sel_species_number)>0:
                        for i in range(self.nmodels):
                            if self.models[i].convType in sel_species_number:
                                ret_data.add_model(self.models[i])
                elif arg.start=='convR':
                    upper=np.nan
                    lower=np.nan
                    if isinstance(arg.stop,float) or isinstance(arg.stop,int):
                        if isinstance(arg.step,float) or isinstance(arg.step,int):
                            lower,upper=arg.stop,arg.step
                        else:
                            upper=arg.stop
                        for i in range(self.nmodels):
                            if not np.isnan(lower):
                                if self.models[i].convR<upper and self.models[i].convR>lower:
                                    ret_data.add_model(self.models[i])
                            else:
                                if self.models[i].convR==upper:
                                    ret_data.add_model(self.models[i])
                    elif isinstance(arg.stop,list):
                        for i in range(self.nmodels):
                            if self.models[i].convR in arg.stop:
                                ret_data.add_model(self.models[i])
                else:
                    raise KeyError('Unrecognised parameter for slicing')
        return ret_data

    def convolve(self,freq_bins=None,R=1,lambda_0=1,lambda_n=1,vr=1300,NLTE=False,conv_type=1,verbose=True,overlap=False):
        for i,d in enumerate(self.models):
            if verbose: print('\n',i+1,'; Model number ',self.models[i].model_number,'; Species number ',self.models[i].species_number)
            d.convolve(freq_bins=freq_bins,R=R,lambda_0=lambda_0,lambda_n=lambda_n,vr=vr,NLTE=NLTE,conv_type=conv_type,overlap=overlap)

    def convolve_overlap(self,R=1,lambda_0=1,lambda_n=1,verbose=True):
        for i,d in enumerate(self.models):
            if verbose: print('\n',i+1,'; Model number ',self.models[i].model_number)
            d.convolve_overlap(R=R,lambda_0=lambda_0,lambda_n=lambda_n)

    def write_to_file(self,filename,mode='line_by_line',verbose=True):
        for i,d in enumerate(self.models):
            d.write_to_file(filename=filename,mode=mode,verbose=verbose)

    @property
    def nmodels(self):
        self._nmodels=len(self.models)
        return self._nmodels

    @nmodels.setter
    def nmodels(self,value):
        self._nmodels=value

    @property
    def species_number(self):
        if self.nmodels>1:
            self._species_number=[]
            for i in range(self.nmodels):
                self._species_number.append(self.models[i].species_number)
        else:
            self._species_number=self.models[0].species_number
        return self._species_number

    @species_number.setter
    def species_number(self,value):
        self._species_number=value

    @property
    def model_number(self):
        if self.nmodels>1:
            self._model_number=[]
            for i in range(self.nmodels):
                self._model_number.append(self.models[i].model_number)
        else:
            self._model_number=self.models[0].model_number
        return self._model_number

    @model_number.setter
    def model_number(self,value):
        self._model_number=value

    @property
    def NH(self):
        if self.nmodels>1:
            self._NH=[]
            for i in range(self.nmodels):
                self._NH.append(self.models[i].NH)
        else:
            self._NH=self.models[0].NH
        return self._NH

    @NH.setter
    def NH(self,value):
        self._NH=value

    @property
    def nColl(self):
        if self.nmodels>1:
            self._nColl=[]
            for i in range(self.nmodels):
                self._nColl.append(self.models[i].nColl)
        else:
            self._nColl=self.models[0].nColl
        return self._nColl

    @nColl.setter
    def nColl(self,value):
        self._nColl=value

    @property
    def ne(self):
        if self.nmodels>1:
            self._ne=[]
            for i in range(self.nmodels):
                self._ne.append(self.models[i].ne)
        else:
            self._ne=self.models[0].ne
        return self._ne

    @ne.setter
    def ne(self,value):
        self._ne=value

    @property
    def nHe(self):
        if self.nmodels>1:
            self._nHe=[]
            for i in range(self.nmodels):
                self._nHe.append(self.models[i].nHe)
        else:
            self._nHe=self.models[0].nHe
        return self._nHe

    @nHe.setter
    def nHe(self,value):
        self._nHe=value

    @property
    def nHII(self):
        if self.nmodels>1:
            self._nHII=[]
            for i in range(self.nmodels):
                self._nHII.append(self.models[i].nHII)
        else:
            self._nHII=self.models[0].nHII
        return self._nHII

    @nHII.setter
    def nHII(self,value):
        self._nHII=value

    @property
    def nHI(self):
        if self.nmodels>1:
            self._nHI=[]
            for i in range(self.nmodels):
                self._nHI.append(self.models[i].nHI)
        else:
            self._nHI=self.models[0].nHI
        return self._nHI

    @nHI.setter
    def nHI(self,value):
        self._nHI=value

    @property
    def nH2(self):
        if self.nmodels>1:
            self._nH2=[]
            for i in range(self.nmodels):
                self._nH2.append(self.models[i].nH2)
        else:
            self._nH2=self.models[0].nH2
        return self._nH2

    @nH2.setter
    def nH2(self,value):
        self._nH2=value

    @property
    def dust_to_gas(self):
        if self.nmodels>1:
            self._dust_to_gas=[]
            for i in range(self.nmodels):
                self._dust_to_gas.append(self.models[i].dust_to_gas)
        else:
            self._dust_to_gas=self.models[0].dust_to_gas
        return self._dust_to_gas

    @dust_to_gas.setter
    def dust_to_gas(self,value):
        self._dust_to_gas=value

    @property
    def vturb(self):
        if self.nmodels>1:
            self._vturb=[]
            for i in range(self.nmodels):
                self._vturb.append(self.models[i].vturb)
        else:
            self._vturb=self.models[0].vturb
        return self._vturb

    @vturb.setter
    def vturb(self,value):
        self._vturb=value

    @property
    def Tg(self):
        if self.nmodels>1:
            self._Tg=[]
            for i in range(self.nmodels):
                self._Tg.append(self.models[i].Tg)
        else:
            self._Tg=self.models[0].Tg
        return self._Tg

    @Tg.setter
    def Tg(self,value):
        self._Tg=value

    @property
    def Td(self):
        if self.nmodels>1:
            self._Td=[]
            for i in range(self.nmodels):
                self._Td.append(self.models[i].Td)
        else:
            self._Td=self.models[0].Td
        return self._Td

    @Td.setter
    def Td(self,value):
        self._Td=value

    @property
    def species_name(self):
        if self.nmodels>1:
            self._species_name=[]
            for i in range(self.nmodels):
                self._species_name.append(self.models[i].species_name)
        else:
            self._species_name=self.models[0].species_name
        return self._species_name

    @species_name.setter
    def species_name(self,value):
        self._species_name=value

    @property
    def species_index(self):
        if self.nmodels>1:
            self._species_index=[]
            for i in range(self.nmodels):
                self._species_index.append(self.models[i].species_index)
        else:
            self._species_index=self.models[0].species_index
        return self._species_index

    @species_index.setter
    def species_index(self,value):
        self._species_index=value

    @property
    def abundance(self):
        if self.nmodels>1:
            self._abundance=[]
            for i in range(self.nmodels):
                self._abundance.append(self.models[i].abundance)
        else:
            self._abundance=self.models[0].abundance
        return self._abundance

    @abundance.setter
    def abundance(self,value):
        self._abundance=value

    @property
    def dv(self):
        if self.nmodels>1:
            self._dv=[]
            for i in range(self.nmodels):
                self._dv.append(self.models[i].dv)
        else:
            self._dv=self.models[0].dv
        return self._dv

    @dv.setter
    def dv(self,value):
        self._dv=value

    @property
    def nlevels(self):
        if self.nmodels>1:
            self._nlevels=[]
            for i in range(self.nmodels):
                self._nlevels.append(self.models[i].nlevels)
        else:
            self._nlevels=self.models[0].nlevels
        return self._nlevels

    @nlevels.setter
    def nlevels(self,value):
        self._nlevels=value

    @property
    def nlines(self):
        if self.nmodels>1:
            self._nlines=[]
            for i in range(self.nmodels):
                self._nlines.append(self.models[i].nlines)
        else:
            self._nlines=self.models[0].nlines
        return self._nlines

    @nlines.setter
    def nlines(self,value):
        self._nlines=value

    @property
    def linedata(self):
        if self.nmodels>1:
            self._linedata=[]
            for i in range(self.nmodels):
                self._linedata.append(self.models[i].linedata)
        else:
            self._linedata=self.models[0].linedata
        return self._linedata

    @linedata.setter
    def linedata(self,value):
        self._linedata=value

    @property
    def leveldata(self):
        if self.nmodels>1:
            self._leveldata=[]
            for i in range(self.nmodels):
                self._leveldata.append(self.models[i].leveldata)
        else:
            self._leveldata=self.models[0].leveldata
        return self._leveldata

    @leveldata.setter
    def leveldata(self,value):
        self._leveldata=value

    @property
    def convWavelength(self):
        if self.nmodels>1:
            self._convWavelength=[]
            for i in range(self.nmodels):
                self._convWavelength.append(self.models[i].convWavelength)
        else:
            self._convWavelength=self.models[0].convWavelength
        return self._convWavelength

    @convWavelength.setter
    def convWavelength(self,value):
        self._convWavelength=value

    @property
    def convLTEflux(self):
        if self.nmodels>1:
            self._convLTEflux=[]
            for i in range(self.nmodels):
                self._convLTEflux.append(self.models[i].convLTEflux)
        else:
            self._convLTEflux=self.models[0].convLTEflux
        return self._convLTEflux

    @convLTEflux.setter
    def convLTEflux(self,value):
        self._convLTEflux=value

    @property
    def convNLTEflux(self):
        if self.nmodels>1:
            self._convNLTEflux=[]
            for i in range(self.nmodels):
                self._convNLTEflux.append(self.models[i].convNLTEflux)
        else:
            self._convNLTEflux=self.models[0].convNLTEflux
        return self._convNLTEflux

    @convNLTEflux.setter
    def convNLTEflux(self,value):
        self._convNLTEflux=value

    @property
    def convType(self):
        if self.nmodels>1:
            self._convType=[]
            for i in range(self.nmodels):
                self._convType.append(self.models[i].convType)
        else:
            self._convType=self.models[0].convType
        return self._convType

    @convType.setter
    def convType(self,value):
        self._convType=value

    @property
    def convR(self):
        if self.nmodels>1:
            self._convR=[]
            for i in range(self.nmodels):
                self._convR.append(self.models[i].convR)
        else:
            self._convR=self.models[0].convR
        return self._convR

    @convR.setter
    def convR(self,value):
        self._convR=value

    @property
    def convOverlapFreq(self):
        if self.nmodels>1:
            self._convOverlapFreq=[]
            for i in range(self.nmodels):
                self._convOverlapFreq.append(self.models[i].convOverlapFreq)
        else:
            self._convOverlapFreq=self.models[0].convOverlapFreq
        return self._convOverlapFreq

    @convOverlapFreq.setter
    def convOverlapFreq(self,value):
        self._convOverlapFreq=value

    @property
    def convOverlapWave(self):
        if self.nmodels>1:
            self._convOverlapWave=[]
            for i in range(self.nmodels):
                self._convOverlapWave.append(self.models[i].convOverlapWave)
        else:
            self._convOverlapWave=self.models[0].convOverlapWave
        return self._convOverlapWave

    @convOverlapWave.setter
    def convOverlapWave(self,value):
        self._convOverlapWave=value

    @property
    def overlapFreq(self):
        if self.nmodels>1:
            self._overlapFreq=[]
            for i in range(self.nmodels):
                self._overlapFreq.append(self.models[i].overlapFreq)
        else:
            self._overlapFreq=self.models[0].overlapFreq
        return self._overlapFreq

    @overlapFreq.setter
    def overlapFreq(self,value):
        self._overlapFreq=value

    @property
    def convOverlapLTE(self):
        if self.nmodels>1:
            self._convOverlapLTE=[]
            for i in range(self.nmodels):
                self._convOverlapLTE.append(self.models[i].convOverlapLTE)
        else:
            self._convOverlapLTE=self.models[0].convOverlapLTE
        return self._convOverlapLTE

    @convOverlapLTE.setter
    def convOverlapLTE(self,value):
        self._convOverlapLTE=value

    @property
    def convOverlapNLTE(self):
        if self.nmodels>1:
            self._convOverlapNLTE=[]
            for i in range(self.nmodels):
                self._convOverlapNLTE.append(self.models[i].convOverlapNLTE)
        else:
            self._convOverlapNLTE=self.models[0].convOverlapNLTE
        return self._convOverlapNLTE

    @convOverlapNLTE.setter
    def convOverlapNLTE(self,value):
        self._convOverlapNLTE=value

    @property
    def overlapLTE(self):
        if self.nmodels>1:
            self._overlapLTE=[]
            for i in range(self.nmodels):
                self._overlapLTE.append(self.models[i].overlapLTE)
        else:
            self._overlapLTE=self.models[0].overlapLTE
        return self._overlapLTE

    @overlapLTE.setter
    def overlapLTE(self,value):
        self._overlapLTE=value

    @property
    def overlapNLTE(self):
        if self.nmodels>1:
            self._overlapNLTE=[]
            for i in range(self.nmodels):
                self._overlapNLTE.append(self.models[i].overlapNLTE)
        else:
            self._overlapNLTE=self.models[0].overlapNLTE
        return self._overlapNLTE

    @overlapNLTE.setter
    def overlapNLTE(self,value):
        self._overlapNLTE=value

    @property
    def overlapTauLTE(self):
        if self.nmodels>1:
            self._overlapTauLTE=[]
            for i in range(self.nmodels):
                self._overlapTauLTE.append(self.models[i].overlapTauLTE)
        else:
            self._overlapTauLTE=self.models[0].overlapTauLTE
        return self._overlapTauLTE

    @overlapTauLTE.setter
    def overlapTauLTE(self,value):
        self._overlapTauLTE=value

    @property
    def overlapTauNLTE(self):
        if self.nmodels>1:
            self._overlapTauNLTE=[]
            for i in range(self.nmodels):
                self._overlapTauNLTE.append(self.models[i].overlapTauNLTE)
        else:
            self._overlapTauNLTE=self.models[0].overlapTauNLTE
        return self._overlapTauNLTE

    @overlapTauNLTE.setter
    def overlapTauNLTE(self,value):
        self._overlapTauNLTE=value

    @property
    def convOverlapR(self):
        if self.nmodels>1:
            self._convOverlapR=[]
            for i in range(self.nmodels):
                self._convOverlapR.append(self.models[i].convOverlapR)
        else:
            self._convOverlapR=self.models[0].convOverlapR
        return self._convOverlapR

    @convOverlapR.setter
    def convOverlapR(self,value):
        self._convOverlapR=value

    @property
    def overlapR(self):
        if self.nmodels>1:
            self._overlapR=[]
            for i in range(self.nmodels):
                self._overlapR.append(self.models[i].overlapR)
        else:
            self._overlapR=self.models[0].overlapR
        return self._overlapR

    @overlapR.setter
    def overlapR(self,value):
        self._overlapR=value


class slab:
    """
    class:: slab
    Class to hold the data of individual slab models
    """

    def __init__(self):
        self.species_number=None
        self.model_number=None
        self.NH=None
        self.nColl=None
        self.ne=None
        self.nHe=None
        self.nHII=None
        self.nHI=None
        self.nH2=None
        self.dust_to_gas=None
        self.vturb=None
        self.Tg=None
        self.Td=None
        self.species_name=None
        self.species_index=None
        self.abundance=None
        self.dv=None
        self.nlevels=None
        self.nlines=None
        self.linedata=None
        self.leveldata=None
        self.convWavelength=None
        self.convLTEflux=None
        self.convNLTEflux=None
        self.convType=None
        self.convR=None
        self.overlapLTE=None
        self.overlapNLTE=None
        self.overlapTauLTE=None
        self.overlapTauNLTE=None
        self.overlapFreq=None
        self.convOverlapLTE=None
        self.convOverlapNLTE=None
        self.convOverlapFreq=None
        self.convOverlapWave=None
        self.convOverlapR=1e5
        self.overlapR=1e5

    def __str__(self):
        output="Info Model: \n"
        output+='species_number= '
        output+=str(self.species_number)+'\n\n'
        output+='model_number  = '
        output+=str(self.model_number)+'\n\n'
        output+='NH            = '
        output+=str(self.NH)+'\n\n'
        output+='nColl         = '
        output+=str(self.nColl)+'\n\n'
        output+='ne            = '
        output+=str(self.ne)+'\n\n'
        output+='nHe           = '
        output+=str(self.nHe)+'\n\n'
        output+='nHII          = '
        output+=str(self.nHII)+'\n\n'
        output+='nHI           = '
        output+=str(self.nHI)+'\n\n'
        output+='nH2           = '
        output+=str(self.nH2)+'\n\n'
        output+='dust_to_gas   = '
        output+=str(self.dust_to_gas)+'\n\n'
        output+='vturb         = '
        output+=str(self.vturb)+'\n\n'
        output+='Tg            = '
        output+=str(self.Tg)+'\n\n'
        output+='Td            = '
        output+=str(self.Td)+'\n\n'
        output+='species_name   = '
        output+=self.species_name+'\n\n'
        output+='abundance     = '
        output+=str(self.abundance)+'\n\n'
        output+='dv            = '
        output+=str(self.dv)+'\n\n'
        output+='nlevels       = '
        output+=str(self.nlevels)+'\n\n'
        output+='nlines        = '
        output+=str(self.nlines)+'\n\n'
        output+='convType       = '
        output+=str(self.convType)+'\n\n'
        output+='convR        = '
        output+=str(self.convR)+'\n\n'
        return output

    def convolve(self,freq_bins=None,R=1,lambda_0=1,lambda_n=1,vr=1300,NLTE=False,conv_type=1,overlap=False):
        if overlap:
            self.convolve_overlap(R=R,lambda_0=lambda_0,lambda_n=lambda_n)
            return
        t='FLTE'
        if NLTE:
            t='FNLTE'
        da=self.linedata
        if lambda_0==lambda_n:
            lambda_0=np.amin(da['GHz']>c/lambda_n*1e-3)
            lambda_n=np.amax(da['GHz']>c/lambda_n*1e-3)
            lambda_0=lambda_0*10**-0.05
            lambda_n=lambda_n*10**0.05
        da_req=da[(da['GHz']>c/lambda_n*1e-3)&(da['GHz']<c/lambda_0*1e-3)]
        da_req.reset_index(drop=True,inplace=True)
        if conv_type==1:
            l,f=generalConvolve(da_req[t],da_req['GHz'],R=R,lambda_0=lambda_0,lambda_n=lambda_n)
        else:
            l,f=specConvolve(da_req[t],da_req['GHz'],freq_bins=freq_bins,R=R,lambda_0=lambda_0,lambda_n=lambda_n,vr=vr)
        self.convWavelength=l
        self.convType=conv_type
        self.convR=R
        if NLTE:
            self.convNLTEflux=f
        else:
            self.convLTEflux=f

    def convolve_overlap(self,R=1,lambda_0=1,lambda_n=1):
        if lambda_0==lambda_n:
            lambda_0=np.amin(c/self.overlapFreq*1e-3)
            lambda_n=np.amax(c/self.overlapFreq*1e-3)
            lambda_0=lambda_0*10**-0.05
            lambda_n=lambda_n*10**0.05
        mask=(self.overlapFreq>c/lambda_n*1e-3)&(self.overlapFreq<c/lambda_0*1e-3)
        FWHM=self.overlapR/R/2.355
        g=Gaussian1DKernel(stddev=FWHM,factor=7)
        self.convOverlapLTE=apy_convolve(self.overlapLTE[mask],g)
        self.convOverlapNLTE=apy_convolve(self.overlapNLTE[mask],g)
        self.convOverlapFreq=self.overlapFreq[mask]*1.0
        self.convOverlapWave=c/self.convOverlapFreq*1e-3
        self.convOverlapR=R

    def write_to_file(self,filename,mode='line_by_line',verbose=True):
        if mode in ['overlap','both']:
            extension = '.fits.gz'
            if not(extension in filename):
                filename_l = filename+extension        
            else:
                filename_l = filename # to avoid that filename_l is not set
            hder = fits.Header(cards=[fits.Card('NMODELS',1)])
            hdu = fits.PrimaryHDU([0.0,0.0],header=hder)
            data = np.zeros((len(self.overlapLTE),5))
            data[:,0] = self.overlapLTE
            data[:,1] = self.overlapTauLTE
            data[:,2] = self.overlapNLTE
            data[:,3] = self.overlapTauNLTE
            data[:,4] = self.overlapFreq
            hder = fits.Header(cards=[fits.Card('NAXIS',2),
                                    fits.Card('NAXIS1',5),
                                    fits.Card('NAXIS2',len(self.overlapLTE)),
                                    fits.Card('MODEL',1),
                                    fits.Card('NLINE',len(self.overlapLTE)),
                                    fits.Card('R_OVLP',self.overlapR),
                                    fits.Card('NHTOT',self.NH),
                                    fits.Card('TG',self.Tg),
                                    fits.Card('TD',10),
                                    fits.Card('VTURB',self.vturb)])
            hdu1 = fits.ImageHDU(data,header=hder)
            hdul = fits.HDUList([hdu,hdu1])
            hdul.writeto(filename_l,overwrite=True)
            if verbose:
                print(f'Output written to {filename_l}')
        
        if mode in ['line_by_line','both']:
            extension = '.out'
            if not(extension in filename):
                filename_l = filename+extension
            else:
                filename_l = filename   # to avoid that filename_l is not set    
            with open(filename_l,'w') as f:
                f.write('1  ! Nmodels\n')
                f.write('1 ! model\n')
                
                f.write('1  ! Number of species\n')
                f.write(f'{self.NH:12.5e} ! Gas column density\n')
                f.write(f'{self.NH:12.5e} ! Total gas density\n')
                f.write(f'{1:12.5e} ! electron density [cm^-3]\n')
                f.write(f'{1:12.5e} ! He density [cm^-3]\n')
                f.write(f'{1:12.5e} ! HII density [cm^-3]\n')
                f.write(f'{1:12.5e} ! HI density [cm^-3]\n')
                f.write(f'{1:12.5e} ! H2 density [cm^-3]\n')
                f.write(f'{1:12.5e} ! dust_to_gas\n')
                f.write(f'{1:12.5e} ! turbulent velocity [km/s]\n')
                f.write(f'{self.Tg:6.1f} ! Tgas [K]\n')
                f.write(f'{0:6.1f} ! Tdust [K]\n')
                f.write(f'{0:d} ! Num\n')
                f.write(f'{self.species_name}\n')
                f.write(f'{1:.1f} ! relative abundance\n')
                f.write(f'{self.vturb*kmps*1e3:12.5e} ! dv [cm/s]\n')
                f.write(f'{int(self.nlevels):12d} ! Nlev\n')
                f.write(f'! i   g       Ener(K)   pop           ltepop      e   v   J\n')
                for i in range(self.nlevels):
                    f.write(f"{i:8d} {self.leveldata.iloc[i]['g']:9.1f} {self.leveldata.iloc[i]['E']:9.1f}{self.leveldata.iloc[i]['pop']:14.5E}{self.leveldata.iloc[i]['ltepop']:14.5E}{int(self.leveldata.iloc[i]['e']):4d} {int(self.leveldata.iloc[i]['v']):4d} {int(self.leveldata.iloc[i]['J']):4d} \n")
                f.write(f'{int(self.nlines):12d} ! Nline\n')
                f.write(f'! i u l e v J gu Eu A B GHz tauD Jback pop ltepop tauNLTE\n')
                f.write(f'tauLTE bNLTE bLTE pNLTE pLTE FNLTE FLTE globU globL locU locL\n')
                for i in range(self.nlines):
                    f.write(f"{i:8d} {int(self.linedata.iloc[i]['u']):8d} {int(self.linedata.iloc[i]['l']):8d} {int(self.linedata.iloc[i]['e']):4d} {int(self.linedata.iloc[i]['v']):4d} {int(self.linedata.iloc[i]['J']):4d} {self.linedata.iloc[i]['gu']:14.5E} {self.linedata.iloc[i]['Eu']:14.5E} {self.linedata.iloc[i]['A']:14.5E} {self.linedata.iloc[i]['B']:14.5E} {self.linedata.iloc[i]['GHz']:14.5E} {self.linedata.iloc[i]['tauD']:14.5E} {self.linedata.iloc[i]['Jback']:14.5E} {self.linedata.iloc[i]['pop']:14.5E} {self.linedata.iloc[i]['ltepop']:14.5E} {self.linedata.iloc[i]['tauNLTE']:14.5E} {self.linedata.iloc[i]['tauLTE']:14.5E} {self.linedata.iloc[i]['bNLTE']:14.5E} {self.linedata.iloc[i]['bLTE']:14.5E} {self.linedata.iloc[i]['pLTE']:14.5E} {self.linedata.iloc[i]['pNLTE']:14.5E} {self.linedata.iloc[i]['FNLTE']:14.5E} {self.linedata.iloc[i]['FLTE']:14.5E} {self.linedata.iloc[i]['global_l']:20} {self.linedata.iloc[i]['global_u']:20} {self.linedata.iloc[i]['local_l']:20} {self.linedata.iloc[i]['local_u']:20} \n")
            if verbose:
                print(f'Output written to {filename_l}')

    def show(self):
        print(self)
        print('lineData    = ')
        print(self.linedata)
        print('levelData   = ')
        print(self.leveldata)


class slab1D:
    """
    class:: slab1D
    Class to hold the data of 1D slab models
    """

    def __init__(self):
        self.directory=None
        self.flux=None
        self.frequency=None
        self.Nspecies=None
        self.species=[]
        self.Ngrid=None
        self.R=None
        self.grid=pd.DataFrame()
        self.source_function=None
        self.source_function_gas=None
        self.tau_dust=None
        self.tau_gas=None
        self.convWavelength=None
        self.convFrequency=None
        self.conv_flux=None
        self.convR=None

    def __str__(self):
        output="Info Model: \n"
        output+='Number of species          = '
        output+=str(self.Nspecies)+'\n\n'
        output+='Grid size                  = '
        output+=str(self.Ngrid)+'\n\n'
        output+='Resolving power of spectra = '
        output+=str(self.R)+'\n\n'
        output+='Output file path = '
        output+=str(self.directory)+'\n\n'
        return output

    def convolve(self,R=1,lambda_0=1,lambda_n=1,verbose=True):
        if verbose: print("Convolving to ",R)
        if lambda_0==lambda_n:
            lambda_0=np.amin(c/self.frequency*1e-3)
            lambda_n=np.amax(c/self.frequency*1e-3)
            lambda_0=lambda_0*10**-0.05
            lambda_n=lambda_n*10**0.05
        mask=(self.frequency>c/lambda_n*1e-3)&(self.frequency<c/lambda_0*1e-3)
        FWHM=self.R/R/2.355
        g=Gaussian1DKernel(stddev=FWHM,factor=7)
        self.conv_flux=apy_convolve(self.flux[mask],g)
        self.convFrequency=self.frequency[mask]*1.0
        self.convR=R
        self.convWavelength=c/self.convFrequency*1e-3

    def show(self):
        print(self)
        print('Grid    = ')
        print(self.grid)
        print('Source function   = ')
        print(self.source_function)
        print('Gas only source function   = ')
        print(self.source_function_gas)
        print('Dust optical depth   = ')
        print(self.tau_dust)
        print('Gas optical depth   = ')
        print(self.tau_gas)


class fit:
    def __init__(self):
        self.name = None
        self.r = None
        self.N = None
        self.T = None
        self.best_fit = None
        self.best_fit_file = None
        self.chi2 = None
        self.fit_window = None
        self.fit_settings = None
        self.chi2_map = None
        self.r_map = None
        
    def __str__(self):
        output = 'Fit: \n'
        output += 'Name: '+str(self.name)+' \n'
        output += 'Best fit parameters: \n'
        output += f'N = {10**self.N:.2e} cm-2, T = {self.T:.1f} K, R = {self.r:.5f} au, chi2 = {self.chi2:.2e} \n'
        output += 'Best fit file: '+str(self.best_fit_file)+'\n'
        output += 'Fit window: '
        if not self.fit_window is None:
            for wind in self.fit_window:
                output += f'{wind[0]:.3f} mic, {wind[1]:.3f} mic\n'
        else:
            output += 'None \n'
        return(output)

        
class fit_settings:
    def __init__(self,NMOL=None,Nlims = [],Tlims = [],grid = None,grid_mask = None,fit_window = None,Rdisk=None,distance=None,R=None,noise_level = None):
        self.NMOL = NMOL
        self.Nlims = Nlims
        self.Tlims = Tlims
        self.grid = grid
        self.grid_mask = grid_mask
        self.fit_window = fit_window
        self.Rdisk = Rdisk
        self.distance = distance
        self.R = R
        self.noise_level = noise_level
        
    def __str__(self):
        output = 'Fit settings: \n'
        output += f'NMOL = {self.NMOL} \n'
        output += f'Nlims = {self.Nlims} \n'
        output += f'Tlims = {self.Tlims} \n'
        output += f'grid.shape = {np.array(self.grid).shape} \n'
        output += f'grid_mask = {self.grid_mask} \n'
        output += f'fit_window = {self.fit_window} \n'
        output += f'len(Rdisk) = {len(self.Rdisk)} \n'
        output += f'distance = {self.distance} \n'
        output += f'R = {self.R} \n'
        output += f'noise_level = {self.noise_level} \n'
        return(output)

        
def read_1D_slab(model_path='SlabResults.fits.gz',verbose=True):
    """
    Function to read 1D prodimo slab model output
    """
    if verbose: print("Reading 1D slab model output from: ",model_path)
    if '.fits.gz' in model_path:
        hdul=fits.open(model_path)
        data=slab1D()
        data.directory=model_path
        data.flux=hdul[0].data.T[:,1]
        data.frequency=hdul[0].data.T[:,0]
        data.Nspecies=hdul[0].header['NSPECIES']
        data.species=hdul[0].header.comments['NSPECIES'].split(',')
        data.Ngrid=hdul[0].header['NGRID']
        data.R=hdul[0].header['R_OVLP']
        if ((9+data.Nspecies*2),data.Ngrid)==hdul[1].data.T.shape:
            grid=hdul[1].data
            data.grid['dz']=grid[:,0]
            data.grid['vturb']=grid[:,1]
            data.grid['nd']=grid[:,2]
            data.grid['Td']=grid[:,3]
            data.grid['nH2']=grid[:,4]
            data.grid['nHI']=grid[:,5]
            data.grid['nHII']=grid[:,6]
            data.grid['nHe']=grid[:,7]
            data.grid['nelec']=grid[:,8]
            for i in range(data.Nspecies):
                key='n'+data.species[i]
                data.grid[key]=grid[:,9+i]
            for i in range(data.Nspecies):
                key='Tg_'+data.species[i]
                data.grid[key]=grid[:,9+data.Nspecies+i]
        else:
            raise AssertionError('Grid in output file does not match the actual grid output array')

        if (len(data.frequency),data.Ngrid)==hdul[2].data.T.shape:
            data.source_function=hdul[2].data
        else:
            raise AssertionError('Source function grid in output file does not match the spatial and frequency grid size')

        if (len(data.frequency),data.Ngrid)==hdul[3].data.T.shape:
            data.source_function_gas=hdul[3].data
        else:
            raise AssertionError('Gas source function grid in output file does not match the spatial and frequency grid size')

        if (len(data.frequency),data.Ngrid)==hdul[4].data.T.shape:
            data.tau_dust=hdul[4].data
        else:
            raise AssertionError('Dust optical depth grid in output file does not match the spatial and frequency grid size')

        if (len(data.frequency),data.Ngrid)==hdul[5].data.T.shape:
            data.tau_gas=hdul[5].data
        else:
            raise AssertionError('Gas optical depth grid in output file does not match the spatial and frequency grid size')
    else:
        data_read=np.loadtxt(model_path,skiprows=1)
        data=slab1D()
        data.directory=model_path
        data.flux=data_read[:,1]
        data.frequency=data_read[:,0]
    return(data)


def read_slab(model_path='SlabResults.out',verbose=True,short_format=False,overlap=False):
    """
    Function to read slab model output
    """
    if overlap or (model_path[-8:]=='.fits.gz'): return(read_overlap_spectra(path=model_path,verbose=verbose))

    if isinstance(model_path,list):
        data=slab_data()
        data.directory=model_path
        for i in model_path:
            rdata=read_slab(i,verbose=verbose,short_format=short_format)
            for j in range(rdata.nmodels):
                data.add_model(rdata.models[j])
        return(data)
    
    
    if verbose: print("Reading slab model output from: ",model_path)
    f=open(model_path)
    data=slab_data()
    nmodels=int(f.readline().split()[0])
    data.directory=model_path
    for i in range(nmodels):
        #tempo                =   slab()
        tempo_model_number=int(f.readline().split()[0])
        nspecies=int(f.readline().split()[0])
        #tempo.species_number =   int(f.readline().split()[0])
        tempo_nHtot=float(f.readline().split()[0])
        tempo_gasDens=float(f.readline().split()[0])
        tempo_nelec=float(f.readline().split()[0])
        tempo_nHe=float(f.readline().split()[0])
        tempo_nHII=float(f.readline().split()[0])
        tempo_nHI=float(f.readline().split()[0])
        tempo_nH2=float(f.readline().split()[0])
        tempo_dust_to_gas=float(f.readline().split()[0])
        tempo_vturb=float(f.readline().split()[0])
        tempo_Tg=float(f.readline().split()[0])
        tempo_Td=float(f.readline().split()[0])
        if short_format:
            for j in range(nspecies):
                tempo=slab()
                tempo.model_number=tempo_model_number
                tempo.NH=tempo_nHtot
                tempo.nColl=tempo_gasDens
                tempo.ne=tempo_nelec
                tempo.nHe=tempo_nHe
                tempo.nHII=tempo_nHII
                tempo.nHI=tempo_nHI
                tempo.nH2=tempo_nH2
                tempo.dust_to_gas=tempo_dust_to_gas
                tempo.vturb=tempo_vturb
                tempo.Tg=tempo_Tg
                tempo.Td=tempo_Td

                tempo.species_index=int(f.readline().split()[0])
                tempo.species_number=j+1
                tempo.species_name=f.readline().split()[0]
                tempo.abundance=float(f.readline().split()[0])
                tempo.dv=float(f.readline().split()[0])
                tempo.nlines=int(f.readline().split()[0])
                lines=f.readline()

                # tempo.nlines=None
                tempo.linedata=None
                tempo.leveldata=None
                tempo.convWavelength=None
                tempo.convLTEflux=None
                tempo.convNLTEflux=None
                tempo.convType=None
                tempo.convR=None

                dat=[]
                # for k in range(tempo.nlevels):
                #     dat[0][k,:]=np.asarray([float(x) for x in f.readline().split()])

                # lines=f.readline()
                # lines=f.readline()
                dat=np.zeros((tempo.nlines,4))
                slabOutFormat=[8,14,15,15]
                for k in range(tempo.nlines):
                    lineRead=[]
                    lines=f.readline()
                    l=0
                    for length in slabOutFormat:
                        lineRead.append(lines[l:l+length])
                        l+=length
                    dat[k,:]=np.asarray([float(x) for x in lineRead])
                lineData=pd.DataFrame(dat,columns=['i','GHz','FNLTE','FLTE'])
                tempo.linedata=lineData
                data.add_model(tempo)
        else:
            for j in range(nspecies):
                tempo=slab()
                tempo.model_number=tempo_model_number
                tempo.NH=tempo_nHtot
                tempo.nColl=tempo_gasDens
                tempo.ne=tempo_nelec
                tempo.nHe=tempo_nHe
                tempo.nHII=tempo_nHII
                tempo.nHI=tempo_nHI
                tempo.nH2=tempo_nH2
                tempo.dust_to_gas=tempo_dust_to_gas
                tempo.vturb=tempo_vturb
                tempo.Tg=tempo_Tg
                tempo.Td=tempo_Td

                tempo.species_index=int(f.readline().split()[0])
                tempo.species_number=j+1
                tempo.species_name=f.readline().split()[0]
                tempo.abundance=float(f.readline().split()[0])
                tempo.dv=float(f.readline().split()[0])
                tempo.nlevels=int(f.readline().split()[0])
                lines=f.readline()

                tempo.nlines=None
                tempo.linedata=None
                tempo.leveldata=None
                tempo.convWavelength=None
                tempo.convLTEflux=None
                tempo.convNLTEflux=None
                tempo.convType=None
                tempo.convR=None

                dat=[np.zeros((tempo.nlevels,8)),[],[]]
                for k in range(tempo.nlevels):
                    dat[0][k,:]=np.asarray([float(x) for x in f.readline().split()])
                tempo.nlines=int(f.readline().split()[0])
                lines=f.readline()
                lines=f.readline()
                dat[1]=np.zeros((tempo.nlines,23))
                slabOutFormat=[9,9,9,5,5,5,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,21,21,21,21]
                for k in range(tempo.nlines):
                    lineRead=[]
                    lines=f.readline()
                    l=0
                    for length in slabOutFormat:
                        lineRead.append(lines[l:l+length])
                        l+=length
                    dat[1][k,:]=np.asarray([float(x) for x in lineRead[0:-4]])
                    dat[2].append([a.strip() for a in lineRead[-4:]])

                lineData=pd.DataFrame(dat[1],columns=['i','u','l','e','v','J','gu','Eu','A','B','GHz','tauD','Jback','pop','ltepop','tauNLTE','tauLTE','bNLTE','bLTE','pNLTE','pLTE','FNLTE','FLTE'])
                lineData['global_u']=[a[0] for a in dat[2]]
                lineData['global_l']=[a[1] for a in dat[2]]
                lineData['local_u']=[a[2] for a in dat[2]]
                lineData['local_l']=[a[3] for a in dat[2]]
                levData=pd.DataFrame(dat[0],columns=['i','g','E','pop','ltepop','e','v','J'])
                tempo.linedata=lineData
                tempo.leveldata=levData
                data.add_model(tempo)
    return(data)


def read_overlap_spectra(path='SlabOverlap.out',verbose=True):
    """
    Function to read 0D prodimo slab model output with line overlap
    """

    if isinstance(path,list):
        data=slab_data()
        data.directory=path
        for i in path:
            rdata=read_overlap_spectra(i,verbose=verbose)
            for j in range(rdata.nmodels):
                data.add_model(rdata.models[j])
        return(data)

    if verbose: print("Reading slab line overlap model output from: ",path)
    if '.fits.gz' in path:
        hdul=fits.open(path)
        data=slab_data()
        nmodels=hdul[0].header['NMODELS']
        data.directory=path
        for i in range(nmodels):
            tempo=slab()
            tempo_model_number=hdul[i+1].header['MODEL']
            tempo_Nline=hdul[i+1].header['NLINE']
            tempo_R=hdul[i+1].header['R_OVLP']
            datta=[]
            tempo.overlapFreq=hdul[i+1].data[:,-1]
            tempo.overlapLTE=hdul[i+1].data[:,0]
            tempo.overlapTauLTE=hdul[i+1].data[:,1]
            tempo.overlapNLTE=hdul[i+1].data[:,2]
            tempo.overlapTauNLTE=hdul[i+1].data[:,3]
            tempo.overlapR=tempo_R
            tempo.model_number=hdul[i+1].header['MODEL']
            tempo.Tg=hdul[i+1].header['TG']
            tempo.Td=hdul[i+1].header['TD']
            tempo.vturb=hdul[i+1].header['VTURB']
            tempo.NH=hdul[i+1].header['NHTOT']
            data.add_model(tempo)
            # print('read ',i,' model')
    else:
        f=open(path)
        data=slab_data()
        nmodels=int(f.readline().split()[0])
        data.directory=path
        for i in range(nmodels):
            tempo=slab()
            tempo_model_number=int(f.readline().split()[0])
            tempo_Nline=int(f.readline().split()[0])
            tempo_R=float(f.readline().split()[0])
            datta=[]
            lines=f.readline()
            for j in range(tempo_Nline):
                lines=f.readline()
                datta.append(np.array(lines.split(),dtype=float))
            datta=np.array(datta)
            tempo.overlapFreq=datta[:,0]
            tempo.overlapLTE=datta[:,1]
            tempo.overlapTauLTE=datta[:,2]
            tempo.overlapNLTE=datta[:,3]
            tempo.overlapTauNLTE=datta[:,4]
            tempo.overlapR=tempo_R
            data.add_model(tempo)
            lines=f.readline()
            # print('read ',i,' model')
    
    return(data)


def specConvolve(lineStrengths,lineFreq,freq_bins=None,R=1,lambda_0=1,lambda_n=1,vr=1300):
    """
    NOT USED ANYMORE
    Function to convolve lines into spectra by simply binning them into a wavelength grid
    """
    gPerc=lambda x,m,s: serf((x-m)/s)*0.5+0.5
    nu_ij=lineFreq*1e9
    if lambda_n==lambda_0:
        lambda_n=np.amax(c/nu_ij*1e6)*2
    if type(freq_bins)==type(None):
        nu=generate_grid(R=R,lambda_0=lambda_0,lambda_n=lambda_n)*1e9
    else:
        freq_bins=np.concatenate((freq_bins,np.array([(freq_bins[-1]-freq_bins[-2])+freq_bins[-1]])))
        nu=freq_bins*1e9
    nu_ij_tile=np.tile(nu_ij,[len(nu),1])
    nu_tile=np.tile(nu,[len(nu_ij),1])
    lineStrengths_tile=np.tile(lineStrengths,[len(nu),1])
    perc_tile=gPerc(nu_tile,nu_ij_tile.T,nu_ij_tile.T/c*vr)
    x=perc_tile[:,:-1]-perc_tile[:,1:]
    wavelength,flux=c/nu[:-1]*1e6,np.sum(x*lineStrengths_tile[:-1,:].T,axis=0)/(nu[:-1]-nu[1:])
    return wavelength,flux


def generalConvolve(lineStrengths,lineFreq,R=1,lambda_0=1,lambda_n=1,R_back=1e6):
    """
    Function to convolve line fluxes into line spectra based on a user defined spectral resolving power R
    """
    if lambda_n==lambda_0:
        lambda_n=c/np.amin(lineFreq)*1e-3*2
    freq_bins=generate_grid(R_back,lambda_0,lambda_n)
    wave_bins=c/freq_bins*1e-3
    flux_bins=wave_bins*0.0
    i=6
    S=lineStrengths
    F=lineFreq
    ind=np.digitize(F,np.flip(freq_bins)[:-1])
    for i,idx in enumerate(ind):
        flux_bins[idx]+=S[i]

    FWHM=R_back/R/2.355
    g=Gaussian1DKernel(stddev=FWHM,factor=7)
    A=apy_convolve(flux_bins,g)
    A=A[1:]/(np.flip(freq_bins)[1:]-np.flip(freq_bins)[:-1])*1e-9
    W=np.flip(wave_bins[1:])
    return np.flip(W),np.flip(A)


def generate_grid(R=1,lambda_0=1,lambda_n=1,sampling=1):
    """
    Generate a spectral grid in GHz
    """
    del_loglam=np.log10(1.0+1.0/R)
    N=1+int(np.log10(lambda_n/lambda_0)/del_loglam)
    mwlsline=np.logspace(np.log10(lambda_0),np.log10(lambda_n),int(N*sampling))
    nu=c/mwlsline*1e6
    return(nu*1e-9)


def convolve(models,freq_bins=None,R=1,lambda_0=1,lambda_n=1,vr=1300,NLTE=False,conv_type=1,verbose=True):
    """
    Same as .convolve() method
    """
    for i,d in enumerate(models):
        if verbose: print('\n\nModel ',i+1)
        d.convolve(freq_bins=freq_bins,R=R,lambda_0=lambda_0,lambda_n=lambda_n,vr=vr,NLTE=NLTE,conv_type=conv_type)
    return models


def generate_slab_grid(directory='.',grid_parameters={},combination=False,Ntot=None,Tg=None,nHplus=None,nH1=None,nH2=None,nHe=None,nelec=None,Td=None,vturb=None,dust_to_gas=None,R_overlap=None,line_overlap=None,species_list={},output_filename='SlabResults.out',overlap_filename='SlabOverlap.out',separate_op_files=True,slab_RT=True,short_format=False,no_individual_lines=False,fits_op_files=False):
    """
    Function to generate SlabInput.in input file containing the details of the slab model grid
    """
    nmodels=1
    combination=False
    if len(grid_parameters)>0:
        if not combination:
            nmodels=len(grid_parameters[list(grid_parameters.keys())[0]])
        else:
            for i in range(len(grid_parameters)):
                nmodels*=len(grid_parameters[list(grid_parameters.keys())[i]])

    Ntot_list=np.ones((nmodels))
    Tg_list=np.ones((nmodels))
    nHplus_list=np.ones((nmodels))
    nH1_list=np.ones((nmodels))
    nH2_list=np.ones((nmodels))
    nHe_list=np.ones((nmodels))
    nelec_list=np.ones((nmodels))
    Td_list=np.ones((nmodels))
    vturb_list=np.ones((nmodels))
    dust_to_gas_list=np.ones((nmodels))
    R_overlap_list=np.ones((nmodels))
    line_overlap_list=np.ones((nmodels,2))
    if len(species_list)<1: raise ValueError('The species_list cannot be empty')

    if not combination:
        for i in range(len(grid_parameters)):
            if list(grid_parameters.keys())[i]=='Ntot':
                Ntot_list*=grid_parameters['Ntot']
            elif list(grid_parameters.keys())[i]=='Tg':
                Tg_list*=grid_parameters['Tg']
            elif list(grid_parameters.keys())[i]=='nHplus':
                nHplus_list*=grid_parameters['nHplus']
            elif list(grid_parameters.keys())[i]=='nH1':
                nH1_list*=grid_parameters['nH1']
            elif list(grid_parameters.keys())[i]=='nH2':
                nH2_list*=grid_parameters['nH2']
            elif list(grid_parameters.keys())[i]=='nHe':
                nHe_list*=grid_parameters['nHe']
            elif list(grid_parameters.keys())[i]=='nelec':
                nelec_list*=grid_parameters['nelec']
            elif list(grid_parameters.keys())[i]=='Td':
                Td_list*=grid_parameters['Td']
            elif list(grid_parameters.keys())[i]=='vturb':
                vturb_list*=grid_parameters['vturb']
            elif list(grid_parameters.keys())[i]=='dust_to_gas':
                dust_to_gas_list*=grid_parameters['dust_to_gas']
            elif list(grid_parameters.keys())[i]=='R_overlap':
                R_overlap_list*=grid_parameters['R_overlap']
            elif list(grid_parameters.keys())[i]=='line_overlap':
                for j in range(len(grid_parameters['line_overlap'])):
                    line_overlap_list[j,:]=np.array(grid_parameters['line_overlap'][j])
            else: raise KeyError(f'Unidentified grid parameter {list(grid_parameters.keys())[i]}')
    else:
        raise KeyError('Combination is still not supported')

    if np.sum(Ntot_list)==nmodels:
        if not (Ntot        is None):
            Ntot_list*=Ntot
        # else:
        #     Ntot_list*=1e15
    if np.sum(Tg_list)==nmodels:
        if not (Tg          is None):
            Tg_list*=Tg
        # else:
        #     Tg_list*=100
    if np.sum(nHplus_list)==nmodels:
        if not (nHplus      is None):
            nHplus_list*=nHplus
        # else:
        #     nHplus_list*=1e1
    if np.sum(nH1_list)==nmodels:
        if not (nH1         is None):
            nH1_list*=nH1
        # else:
        #     nH1_list*=1e12
    if np.sum(nH2_list)==nmodels:
        if not (nH2         is None):
            nH2_list*=nH2
        # else:
        #     nH2_list*=1e12
    if np.sum(nHe_list)==nmodels:
        if not (nHe         is None):
            nHe_list*=nHe
        # else:
        #     nHe_list*=1e11
    if np.sum(nelec_list)==nmodels:
        if not (nelec       is None):
            nelec_list*=nelec
        # else:
        #     nelec_list*=1e8
    if np.sum(Td_list)==nmodels:
        if not (Td          is None):
            Td_list*=Td
        # else:
        #     Td_list*=10
    if np.sum(vturb_list)==nmodels:
        if not (vturb       is None):
            vturb_list*=vturb
        # else:
        #     vturb_list*=1.4
    if np.sum(dust_to_gas_list)==nmodels:
        if not (dust_to_gas is None):
            dust_to_gas_list*=dust_to_gas
        # else:
        #     dust_to_gas_list*=1e-21
    if np.sum(R_overlap_list)==nmodels:
        if not (R_overlap is None):
            R_overlap_list*=R_overlap
        # else:
        #     R_overlap_list*=1e5
    if np.sum(line_overlap_list)==2*nmodels:
        if not (line_overlap is None):
            line_overlap_list*=np.array(line_overlap)
        # else:
        #     line_overlap_list*=np.array((4,30))

    os.system(f'touch {directory+"/SlabInput.in"}')
    f=open(directory+'/SlabInput.in','w')
    f.write("***********************************************************\n")
    f.write("*** Input file for slab escape probability with ProDiMo ***\n")
    f.write("***********************************************************\n")
    f.write("*** nmodels should follow output_filename ***\n")
    f.write(f'{output_filename} ! output_filename\n')
    f.write(f'{overlap_filename} ! overlap_filename\n')
    if separate_op_files:
        f.write('.true.    ! separate_op_files\n')
    else:
        f.write('.false.   ! separate_op_files\n')
    if fits_op_files:
        f.write('.true.    ! fits_op_files\n')
    else:
        f.write('.false.   ! fits_op_files\n')
    if no_individual_lines:
        f.write('.true.    ! no_individual_lines\n')
    else:
        f.write('.false.   ! no_individual_lines\n')
    if slab_RT:
        f.write('.true.    ! slab_RT \n')
    else:
        f.write('.false.   ! slab_RT \n')
    if short_format:
        f.write('.true.    ! short_format\n')
    else:
        f.write('.false.   ! short_format\n')
    f.write(f'{nmodels}             ! nmodels\n')
    f.write('-------------------------------------------------------')
    for i in range(nmodels):
        f.write(f'\n*** model {i+1} ***\n')
        if np.sum(Ntot_list)!=nmodels:
            f.write(fmt.format('{:.3m}',Ntot_list[i]))
            f.write('	   ! NHtot  [cm^-2] total gas column density\n')
        if np.sum(nHplus_list)!=nmodels:
            f.write(fmt.format('{:.3m}',nHplus_list[i]))
            f.write('	   ! nH+    [cm^-3]  proton number density\n')
        if np.sum(nH1_list)!=nmodels:
            f.write(fmt.format('{:.3m}',nH1_list[i]))
            f.write('	   ! nHI	 [cm^-3] atomic hydrogen\n')
        if np.sum(nH2_list)!=nmodels:
            f.write(fmt.format('{:.3m}',nH2_list[i]))
            f.write('	   ! nH2    [cm^-3]   molecular hydrogen\n')
        if np.sum(nHe_list)!=nmodels:
            f.write(fmt.format('{:.3m}',nHe_list[i]))
            f.write('	   ! nHe    [cm^-3]   Helium\n')
        if np.sum(nelec_list)!=nmodels:
            f.write(fmt.format('{:.3m}',nelec_list[i]))
            f.write('	   ! nelec  [cm^-3]   electron number density\n')
        if np.sum(Tg_list)!=nmodels:
            f.write(fmt.format('{:.3m}',Tg_list[i]))
            f.write('	   ! Tgas [K]           gas temperature\n')
        if np.sum(Td_list)!=nmodels:
            f.write(fmt.format('{:.3m}',Td_list[i]))
            f.write('	   ! Tdust [K]           dust temperature\n')
        if np.sum(vturb_list)!=nmodels:
            f.write(fmt.format('{:.3m}',vturb_list[i]))
            f.write('	   ! vturb  [kms/s]    turbulent velocity\n')
        if np.sum(dust_to_gas_list)!=nmodels:
            f.write(fmt.format('{:.3m}',dust_to_gas_list[i]))
            f.write('	   ! dust_to_gas\n')
        if np.sum(line_overlap_list)!=2*nmodels:
            f.write(fmt.format('{:.3f}',line_overlap_list[i,0])+' '+fmt.format('{:.3f}',line_overlap_list[i,1]))
            f.write('	   ! line_overlap  [microns]  minimum and maximum wavelengths for line overlap\n')
        if np.sum(R_overlap_list)!=nmodels:
            f.write(fmt.format('{:.3m}',R_overlap_list[i]))
            f.write('	   ! R_overlap  sampling grid resolution for line overlap\n')
        f.write(f'{len(species_list)}	   ! Nspecies            number of species for that model\n')
        for j in range(len(species_list)):
            f.write(f'{list(species_list.keys())[j]}      {species_list[list(species_list.keys())[j]]}\n')
        f.write('           ! end\n')
        f.write('-------------------------------------------------------')
    f.close()
    return


def generate_1D_structure(dz,species_list,vturb,nd,Td,n_species,T_species,nH2=0,nHI=0,nHII=0,nHe=0,nelec=0,filename='1D_structure'):
    """
    Generates 1D structure file required for 1D slab models
    """
    if isinstance(dz,float) or isinstance(dz,int): dz=np.array([dz])
    if isinstance(dz,list): dz=np.array(dz)
    if isinstance(species_list,str): species_list=[species_list]
    if isinstance(vturb,float) or isinstance(vturb,int): vturb=np.ones_like(dz)*vturb
    if isinstance(nd,float) or isinstance(nd,int): nd=np.ones_like(dz)*nd
    if isinstance(Td,float) or isinstance(Td,int): Td=np.ones_like(dz)*Td
    if isinstance(nH2,float) or isinstance(nH2,int): nH2=np.ones_like(dz)*nH2
    if isinstance(nHI,float) or isinstance(nHI,int): nHI=np.ones_like(dz)*nHI
    if isinstance(nHII,float) or isinstance(nHII,int): nHII=np.ones_like(dz)*nHII
    if isinstance(nHe,float) or isinstance(nHe,int): nHe=np.ones_like(dz)*nHe
    if isinstance(nelec,float) or isinstance(nelec,int): nelec=np.ones_like(dz)*nelec
    if isinstance(n_species,float) or isinstance(n_species,int): n_species=np.ones((dz.shape[0],len(species_list)))*n_species
    if isinstance(T_species,float) or isinstance(T_species,int): T_species=np.ones((dz.shape[0],len(species_list)))*T_species
    if isinstance(T_species,list): T_species=np.array(T_species)
    if isinstance(n_species,list): n_species=np.array(n_species)
    if np.array(T_species).size==len(species_list):
        T_species_temp=np.ones((dz.shape[0],len(species_list)))
        for i in range(len(species_list)):
            T_species_temp[:,i]=T_species[i]
        T_species=T_species_temp*1.00
    if np.array(n_species).size==len(species_list):
        n_species_temp=np.ones((dz.shape[0],len(species_list)))
        for i in range(len(species_list)):
            n_species_temp[:,i]=n_species[i]
        n_species=n_species_temp*1.00

    with open(filename,'w') as f:
        f.write(f'{len(dz):d}\n')
        f.write(f'{len(species_list):d}\n')
        for i in range(len(species_list)):
            f.write(species_list[i]+'\n')
        for i in range(len(dz)):
            string=''
            string+=f'{i+1:d}  '
            string+=f'{dz[i]:.3e}  '
            string+=f'{vturb[i]:.3f}  '
            string+=f'{nd[i]:.3e}  '
            string+=f'{Td[i]:.3f}  '
            for j in range(len(species_list)):
                string+=f'{n_species[i,j]:.3e}  '
            for j in range(len(species_list)):
                string+=f'{T_species[i,j]:.3f}  '
            string+=f'{nH2[i]:.3e}  '
            string+=f'{nHI[i]:.3e}  '
            string+=f'{nHII[i]:.3e}  '
            string+=f'{nHe[i]:.3e}  '
            string+=f'{nelec[i]:.3e}  '
            f.write(string+'\n')
        f.close()


def line_flux(l1,l2,wavelength,flux):
    '''
    Units: Return is in the same unit as input. [Assumed to be in erg/s/cm2/sr] l1 and l2 same unit as wavelength

    Returns
    -------
    float:
      Sum of integrated line flux between wavelengths l1 and l2.

    '''
    mask=(wavelength>l1)&(wavelength<=l2)
    return np.sum(flux[mask])


def line_fluxes(windows,wavelength,flux):
    '''
    Return: array of sum of integrated line flux in wavelength windows.

    Units: Return is in the same unit as input. [Assumed to be in erg/s/cm2/sr]

    windows: list of wavelength limits of windows. Example: [[14,14.5],[15,16.2],[12.5,14.1]]
    '''
    F=[]
    for W in windows:
        F.append(line_flux(W[0],W[1],wavelength,flux))
    return(np.array(F))


def line_flux_ratios(ratio_windows,wavelength,flux):
    '''
    Return: Integrated line flux ratios between wavelengths l1 and l2.

    Unit: Return has no unit. [Input is assumed to be in erg/s/cm2/sr]

    ratio_windows: list of wavelength windows. Example: [[[14,14.5],[15,16.2]],[[12.5,14.1],[13.4,13.8]]]
    '''
    R=[]
    for window in ratio_windows:
        F=line_fluxes([window[0],window[1]],wavelength,flux)
        R.append(F[1]/F[0])
    return(np.array(R))


def line_flux_products(product_windows,wavelength,flux):
    '''
    Return: Integrated line flux products between wavelengths l1 and l2.

    Unit: Return unit is output units squared. [Input is assumed to be in erg/s/cm2/sr]

    product_windows: list of wavelength windows. Example: [[[14,14.5],[15,16.2]],[[12.5,14.1],[13.4,13.8]]]
    '''
    R=[]
    for window in product_windows:
        F=line_fluxes([window[0],window[1]],wavelength,flux)
        R.append(F[1]*F[0])
    return(np.array(R))


def spectral_flux(l1,l2,wavelength,flux):
    '''
    Unit: Return in [erg/s/cm2] and input is in [Jy] l1, l2, and wavelength in microns

    Returns
    -------
    float:
      Sum of integrated line flux between wavelengths l1 and l2.

    '''
    flux=flux*1e-23  # Converting Jy to erg.s−1.cm−2.Hz−1
    wavelength=wavelength*1e-4  # Converting microns to cm
    flux=flux[np.argsort(wavelength)]
    wavelength=wavelength[np.argsort(wavelength)]
    l1=l1*1e-4  # Converting microns to cm
    l2=l2*1e-4  # Converting microns to cm
    c_cms=c*1e2  # Converting m/s to cm/s
    mask=(wavelength>l1)&(wavelength<=l2)
    wave=wavelength[mask]
    # wave1      = np.roll(wavelength,1)[mask]
    # wave1      = 10**((np.log10(wave)+np.log10(wave1))/2)
    # wave2      = np.roll(wavelength,-1)[mask]
    # wave2      = 10**((np.log10(wave)+np.log10(wave2))/2)
    # dnu        = c*(wave2-wave1)/wave**2*1e2
    wave1=np.roll(wavelength,1)[mask]
    wave2=np.roll(wavelength,-1)[mask]
    dnu=(c_cms*(1/wave1-1/wave2)/2)
    return(np.sum(flux[mask]*dnu))


def spectral_fluxes(windows,wavelength,flux):
    '''
    Return: Sum of integrated line flux between wavelength windows.

    Unit: return is in [erg/s/cm2] and input is in [Jy]

    windows: list of wavelength limits (microns) of windows. Example: [[14,14.5],[15,16.2],[12.5,14.1]]
    '''
    F=[]
    for W in windows:
        F.append(spectral_flux(W[0],W[1],wavelength,flux))
    return(np.array(F))


def spectral_flux_ratios(ratio_windows,wavelength,flux):
    '''
    Return: Spectral integrated flux ratios between wavelength windows.

    Units: Return is without units and input is in [Jy]

    ratio_windows: list of wavelength (microns) windows. Example: [[[14,14.5],[15,16.2]],[[12.5,14.1],[13.4,13.8]]]
    '''
    R=[]
    for window in ratio_windows:
        F=spectral_fluxes([window[0],window[1]],wavelength,flux)
        R.append(F[1]/F[0])
    return(np.array(R))


def spectral_flux_products(product_windows,wavelength,flux):
    '''
    Return: Products of spectral integrated fluxes between wavelength windows.

    Units: Return unit is output units squared and input is in [Jy]

    product_windows: list of wavelength (microns) windows. Example: [[[14,14.5],[15,16.2]],[[12.5,14.1],[13.4,13.8]]]
    '''
    R=[]
    for window in product_windows:
        F=spectral_fluxes([window[0],window[1]],wavelength,flux)
        R.append(F[1]*F[0])
    return(np.array(R))


def chi2_slab(slab_data,spectra,windows=[],ratio_windows=[],product_windows=[],Rdisk=np.logspace(-2,2,10),distance=120,convolve=False,NLTE=False,short_format=False):
    '''
    Returns chi2 based on selected spectral windows across different emitting disk radius

    Parameters
    ----------
    slab_data : string or slab_model instance
      path corresponding to a single slab model or a single slab_model instance

    spectra : numpy.array
      numpy array with first column the wavelength in [microns] and second column flux in [Jy]

    windows : array_like
      List of spectral windows for chi2 calculation (weights optional). Format : [window1,window2,....]
      Window format: [lambda_0, lambda_1, weight] weight is optional, used for weighted chi2
      Example without weight: [[14,14.5],[15,16.2],[12.5,14.1]]
      Example with weight: [[14,14.5,2],[15,16.2,5],[12.5,14.1,1]]
      Weights are automatically normalised, so sum of weights need not be 1

    Rdisk : array_like
      Radius corresponding to emitting area in astronomical units

    distance : float
      distance of disk in parsec

    convolve : boolean
      If True, the chi2 is performed on convolved spectra and not on individual lines

    NLTE : boolean
      if True, NLTE flux is taken from the slab model.
    '''
    area=np.pi*(Rdisk*au/distance/pc)**2
    chi_area=np.zeros((len(area)))
    if isinstance(slab_data,str): slab_data=read_slab(slab_data,verbose=False,short_format=short_format)
    if len(windows)<0 and len(ratio_windows)<0 and len(product_windows)<0: return chi_area
    if convolve:  # to estimate flux from convolved spectra
        lmin,lmax=[],[]
        if len(windows)>0:
            lmin.append(np.amin(np.array([[i[0],i[1]] for i in windows]).flatten()))
            lmax.append(np.amax(np.array([[i[0],i[1]] for i in windows]).flatten()))
        if len(ratio_windows)>0:
            lmin.append(np.amin(np.array([[i[0],i[1]] for i in ratio_windows]).flatten()))
            lmax.append(np.amax(np.array([[i[0],i[1]] for i in ratio_windows]).flatten()))
        if len(product_windows)>0:
            lmin.append(np.amin(np.array([[i[0],i[1]] for i in product_windows]).flatten()))
            lmax.append(np.amax(np.array([[i[0],i[1]] for i in product_windows]).flatten()))
        lmin=np.amin(lmin)
        lmax=np.amax(lmax)
        slab_data.convolve(R=2000,lambda_0=lmin*0.9,lambda_n=lmax*1.1,NLTE=NLTE,verbose=False)
        if NLTE:
            Fmodel=spectral_fluxes(windows,slab_data.convWavelength,slab_data.convNLTEflux*1e23)
            Rmodel=spectral_flux_ratios(ratio_windows,slab_data.convWavelength,slab_data.convNLTEflux*1e23)
            Pmodel=spectral_flux_products(product_windows,slab_data.convWavelength,slab_data.convNLTEflux*1e23)
        else:
            Fmodel=spectral_fluxes(windows,slab_data.convWavelength,slab_data.convLTEflux*1e23)
            Rmodel=spectral_flux_ratios(ratio_windows,slab_data.convWavelength,slab_data.convLTEflux*1e23)
            Pmodel=spectral_flux_products(product_windows,slab_data.convWavelength,slab_data.convLTEflux*1e23)
    else:  # to estimate flux from line list
        if NLTE:
            t='FNLTE'
        else:
            t='FLTE'
        linedata=slab_data.linedata
        linedata.sort_values(by=['GHz'],ascending=False,inplace=True,ignore_index=True)
        Fmodel=line_fluxes(windows,c/linedata['GHz']*1e-3,linedata[t])
        Rmodel=line_flux_ratios(ratio_windows,c/linedata['GHz']*1e-3,linedata[t])
        Pmodel=line_flux_ratios(product_windows,c/linedata['GHz']*1e-3,linedata[t])
    Fobserved=spectral_fluxes(windows,spectra[:,0],spectra[:,1])
    Robserved=spectral_flux_ratios(ratio_windows,spectra[:,0],spectra[:,1])
    Pobserved=spectral_flux_products(product_windows,spectra[:,0],spectra[:,1])
    norm_factor=0
    if len(windows)>0:
        area_2d=np.dstack([area for i in range(len(windows))]).squeeze().reshape((len(area),len(windows)))
        Fmodel_2d=np.dstack([Fmodel for i in range(len(area))]).squeeze().T.reshape((len(area),len(windows)))
        Fobserved_2d=np.dstack([Fobserved for i in range(len(area))]).squeeze().T.reshape((len(area),len(windows)))
        if len(windows[0])==3:  # weighted chi2
            windows_weights=np.array([windows[k][2] for k in range(len(windows))])
            windows_weights_2d=np.dstack([windows_weights for i in range(len(area))]).squeeze().T.reshape((len(area),len(windows_weights)))
            chi_area+=np.sum(((Fmodel_2d*area_2d-Fobserved_2d)/Fobserved_2d)**2*windows_weights_2d,axis=1)
            norm_factor+=np.sum(windows_weights)
        else:
            chi_area+=np.sum(((Fmodel_2d*area_2d-Fobserved_2d)/Fobserved_2d)**2,axis=1)
            norm_factor+=len(windows)
    if len(ratio_windows)>0:
        Rmodel_2d=np.dstack([Rmodel for i in range(len(area))]).squeeze().T.reshape((len(area),len(ratio_windows)))
        Robserved_2d=np.dstack([Robserved for i in range(len(area))]).squeeze().T.reshape((len(area),len(ratio_windows)))
        if (len(ratio_windows[0])==3):  # weighted chi2
            ratio_windows_weights=np.array([ratio_windows[k][2] for k in range(len(ratio_windows))])
            ratio_windows_weights_2d=np.dstack([ratio_windows_weights for i in range(len(area))]).squeeze().T.reshape((len(area),len(ratio_windows_weights)))
            chi_area+=np.sum(((Rmodel_2d-Robserved_2d)/Robserved_2d)**2*ratio_windows_weights_2d,axis=1)
            norm_factor+=np.sum(ratio_windows_weights)
        else:
            chi_area+=np.sum(((Rmodel_2d-Robserved_2d)/Robserved_2d)**2,axis=1)
            norm_factor+=len(ratio_windows)
    if len(product_windows)>0:
        area_2d=np.dstack([area for i in range(len(product_windows))]).squeeze().reshape((len(area),len(product_windows)))
        Pmodel_2d=np.dstack([Pmodel for i in range(len(area))]).squeeze().T.reshape((len(area),len(product_windows)))
        Pobserved_2d=np.dstack([Pobserved for i in range(len(area))]).squeeze().T.reshape((len(area),len(product_windows)))
        if (len(product_windows[0])==3):  # weighted chi2
            product_windows_weights=np.array([product_windows[k][2] for k in range(len(product_windows))])
            product_windows_weights_2d=np.dstack([product_windows_weights for i in range(len(area))]).squeeze().T.reshape((len(area),len(product_windows_weights)))
            chi_area+=np.sum((((Pmodel_2d*area_2d**2)**0.5-(Pobserved_2d)**0.5)/(Pobserved_2d)**0.5)**2*product_windows_weights_2d,axis=1)
            norm_factor+=np.sum(product_windows_weights)
        else:
            chi_area+=np.sum((((Pmodel_2d*area_2d**2)**0.5-(Pobserved_2d)**0.5)/(Pobserved_2d)**0.5)**2,axis=1)
            norm_factor+=len(product_windows)
    if norm_factor>0: chi_area/=norm_factor
    return(chi_area)


def red_chi2_slab(slab_data,spectra,mask,Rdisk=np.logspace(-2,2,10),distance=120,NLTE=False,R=3000,short_format=False,overlap=False,noise_level=1):
    '''
    Returns reduced chi2 based on selected spectral windows across different emitting disk radius

    Parameters
    ----------
    slab_data : string or slab_model instance
      path corresponding to a single slab model or a single slab_model instance
    
    spectra : numpy.array
      numpy array with first column the wavelength in [microns] and second column flux in [Jy]

    mask : numpy.array
      numpy boolean array that masks certain parts of the spectra from the fit  
    
    Rdisk : float
      Radius corresponding to emitting area in astronomical units
    
    distance : float
      distance of disk in parsec
    
    NLTE : boolean
      if True, NLTE flux is taken from the slab model in case of overlap=False.

    R : float
      Spectral resolving power of the observed spectrum for convolving the slab model
    
    short_format : boolean
      Type of slab model output file, short vs long
    
    overlap : boolean
      Molecular opacity overlap considered in the slab model
      
    noise_level : float
      Noise level in the spectrum, in the same units as the flux passed in the argument spectra
    '''
    area=(np.pi*(Rdisk*au/distance/pc)**2).reshape(Rdisk.shape[0],1)

    if isinstance(slab_data,str): slab_data=read_slab(slab_data,verbose=False,short_format=short_format,overlap=overlap)
    lmin=np.amin(spectra[:,0])
    lmax=np.amax(spectra[:,0])
    slab_data.convolve(R=R,lambda_0=lmin*0.9,lambda_n=lmax*1.1,NLTE=NLTE,verbose=False,overlap=overlap)
    if not overlap:
        if NLTE:
            modelSpec=spectres(spectra[:,0],slab_data.convWavelength,slab_data.convNLTEflux*1e23,verbose=False,fill=0.0)
        else:
            modelSpec=spectres(spectra[:,0],slab_data.convWavelength,slab_data.convLTEflux*1e23,verbose=False,fill=0.0)
    else:
        modelSpec=spectres(spectra[:,0],c/slab_data.convOverlapFreq[::-1]*1e-3,slab_data.convOverlapLTE[::-1]*1e23,verbose=False,fill=0.0)
    spectra_2d=spectra[mask,1].reshape(1,spectra[mask,-1].shape[0])*np.ones_like(area)
    modelSpec_2d=modelSpec[mask].reshape(1,modelSpec[mask].shape[0])*np.ones_like(area)
    area_2d=area.reshape(area.shape[0],1)
    chi_area=np.sum((spectra_2d-modelSpec_2d*area_2d)**2,axis=1)/len(spectra[mask,0])/noise_level**2

    return(chi_area)


def red_chi2_slab_weighted(slab_data,spectra,mask_weight_array,Rdisk=np.logspace(-2,2,10),distance=120,NLTE=False,R=3000,short_format=False,overlap=False,noise_level=1):
    '''
    Returns reduced chi2 based on selected spectral windows across different emitting disk radius

    Parameters
    ----------
    slab_data : string or slab_model instance
      path corresponding to a single slab model or a single slab_model instance
    
    spectra : numpy.array
      numpy array with first column the wavelength in [microns] and second column flux in [Jy]

    mask_array : list of list [numpy.array,float]
      list containing lists of numpy boolean arrays that masks certain parts of the spectra from the fit and their weighting  
    
    Rdisk : float
      Radius corresponding to emitting area in astronomical units
    
    distance : float
      distance of disk in parsec
    
    NLTE : boolean
      if True, NLTE flux is taken from the slab model in case of overlap=False.

    R : float
      Spectral resolving power of the observed spectrum for convolving the slab model
    
    short_format : boolean
      Type of slab model output file, short vs long
    
    overlap : boolean
      Molecular opacity overlap considered in the slab model
      
    noise_level : float
      Noise level in the spectrum, in the same units as the flux passed in the argument spectra
    '''
    area=(np.pi*(Rdisk*au/distance/pc)**2).reshape(Rdisk.shape[0],1)

    if isinstance(slab_data,str): slab_data=read_slab(slab_data,verbose=False,short_format=short_format,overlap=overlap)
    lmin=np.amin(spectra[:,0])
    lmax=np.amax(spectra[:,0])
    slab_data.convolve(R=R,lambda_0=lmin*0.9,lambda_n=lmax*1.1,NLTE=NLTE,verbose=False,overlap=overlap)
    if not overlap:
        if NLTE:
            modelSpec=spectres(spectra[:,0],slab_data.convWavelength,slab_data.convNLTEflux*1e23,verbose=False,fill=0.0)
        else:
            modelSpec=spectres(spectra[:,0],slab_data.convWavelength,slab_data.convLTEflux*1e23,verbose=False,fill=0.0)
    else:
        modelSpec=spectres(spectra[:,0],c/slab_data.convOverlapFreq[::-1]*1e-3,slab_data.convOverlapLTE[::-1]*1e23,verbose=False,fill=0.0)
    chi_area = np.zeros_like(Rdisk)
    weight_array = []
    for [mask,weight] in mask_weight_array:
        spectra_2d=spectra[mask,1].reshape(1,spectra[mask,-1].shape[0])*np.ones_like(area)
        modelSpec_2d=modelSpec[mask].reshape(1,modelSpec[mask].shape[0])*np.ones_like(area)
        area_2d=area.reshape(area.shape[0],1)
        chi_area+=np.sum((spectra_2d-modelSpec_2d*area_2d)**2,axis=1)/len(spectra[mask,0])/noise_level**2*weight
        weight_array.append(weight)

    return(chi_area/np.sum(weight_array))


def red_chi2_slab_multi(slab_data,spectra,mask,Rdisk=np.logspace(-2,2,10),distance=120,NLTE=False,R=3000,short_format=False,overlap=False,noise_level=1):
    '''
    Returns reduced chi2 for two slab models based on selected spectral windows across different emitting disk radius

    Parameters
    ----------
    slab_data : list of strings
      paths corresponding to two slab model
    spectra : numpy.array
      numpy array with first column the wavelength in [microns] and second column flux in [Jy]

    mask : numpy.array
      numpy boolean array that masks certain parts of the spectra from the fit  
    
    Rdisk : float
      Radius corresponding to emitting area in astronomical units
    
    distance : float
      distance of disk in parsec
    
    NLTE : boolean
      if True, NLTE flux is taken from the slab model in case of overlap=False.

    R : float
      Spectral resolving power of the observed spectrum for convolving the slab model
    
    short_format : boolean
      Type of slab model output file, short vs long
    
    overlap : boolean
      Molecular opacity overlap considered in the slab model
      
    noise_level : float
      Noise level in the spectrum, in the same units as the flux passed in the argument spectra
    '''
    area = (np.pi*(Rdisk*au/distance/pc)**2).reshape(Rdisk.shape[0],1,1)
    fraction = np.linspace(0,1,100).reshape(1,100,1)
    if isinstance(slab_data,str): 
        slab_data=read_slab(slab_data,verbose=False,short_format=short_format,overlap=overlap)
    elif isinstance(slab_data,list):
        slab_data=read_slab(slab_data,verbose=False,short_format=short_format,overlap=overlap)
        
    lmin=np.amin(spectra[:,0])
    lmax=np.amax(spectra[:,0])
    slab_data.convolve(R=R,lambda_0=lmin*0.9,lambda_n=lmax*1.1,NLTE=NLTE,verbose=False,overlap=overlap)
    if not overlap:
        if NLTE:
            contSpec = spectres(spectra[:,0], slab_data[0].convWavelength,slab_data[0].convNLTEflux*1e23,verbose=False,fill=0.0)
            featSpec = spectres(spectra[:,0], slab_data[1].convWavelength,slab_data[1].convNLTEflux*1e23,verbose=False,fill=0.0)
        else:
            contSpec = spectres(spectra[:,0], slab_data[0].convWavelength,slab_data[0].convLTEflux*1e23,verbose=False,fill=0.0)
            featSpec = spectres(spectra[:,0], slab_data[1].convWavelength,slab_data[1].convLTEflux*1e23,verbose=False,fill=0.0)
    else:
        contSpec = spectres(spectra[:,0], slab_data[0].convOverlapWave[::-1],slab_data[0].convOverlapLTE[::-1]*1e23, verbose=False,fill=0.0)
        featSpec = spectres(spectra[:,0], slab_data[1].convOverlapWave[::-1],slab_data[1].convOverlapLTE[::-1]*1e23, verbose=False,fill=0.0)
    
    spectra  = spectra[mask,1].reshape(1,1,spectra[mask,-1].shape[0])
    contSpec =  contSpec[mask].reshape(1,1,contSpec[mask].shape[0])
    featSpec =  featSpec[mask].reshape(1,1,featSpec[mask].shape[0])
    
    finalSpec = area*(fraction*contSpec+(1-fraction)*featSpec)
    chi_area = np.sum((spectra-finalSpec)**2,axis=2)/spectra.size/noise_level**2
    
    return(chi_area)

