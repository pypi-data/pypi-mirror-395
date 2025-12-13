"""
.. module:: hitran
   :synopsis: Read routines and data structure for prodimo HITRAN datafiles.

.. moduleauthor:: A. M. Arabhavi


"""

import numpy as np
import pandas as pd
from scipy.constants import h,c,k
from itertools import compress

class selection_rules:
    '''
    Stores line selection rules following the format prescribed by |prodimo| for writing LineSelection.in files
    '''
    def __init__(self):
        self._name = None
        self._prodimo_name = None
        self._iso = int(1)
        self._mass = None
        self._waveSelection = None
        self._ESelection = None
        self._bandSelection = None
        self._hitran_min_strength = None
        self._file = None
        self._custom_partition_sum = None
        self._output_file = None
        self._custom = False
        self._abundance_fraction = 1.0

    def __str__(self):
        output = 'Selection rule:\n'
        output += 'Name: '+self._name+'\n'
        output += 'iso: '+str(self._iso)+'\n'
        output += 'mass: '+str(self._mass)+'\n'
        output += 'abundance_fraction: '+str(self._abundance_fraction)+'\n'
        if not (self._waveSelection is None):
            output += 'Wavelength selection: '+ str(len(self._waveSelection)) + '\n'
            for i in range(len(self._waveSelection)):
                output += f'[{self._waveSelection[i][0]} {self._waveSelection[i][1]}]\n'
        if not (self._ESelection is None):
            output += 'Upper energy selection: '+ str(len(self._ESelection)) + '\n'
            for i in range(len(self._ESelection)):
                output += f'[{self._ESelection[i][0]} {self._ESelection[i][1]}]\n'
        if not (self._bandSelection is None):
            output += 'Band selection: '+ str(len(self._bandSelection)) + '\n'
            for i in range(len(self._bandSelection)):
                output += f'{self._bandSelection[i][0]} <-> {self._bandSelection[i][1]}\n'
        output += 'hitran min strength: '+f'{self._hitran_min_strength:6.2e}'+'\n'
        if not (self._file is None):
            output += 'file: '+self._file+'\n'
        if not (self._output_file is None):
            output += 'output_file: '+self._output_file+'\n'
        if not (self._custom_partition_sum is None):
            output += 'custom_partition_sum: '+self._custom_partition_sum+'\n'
        if self._custom:
            output += 'custom molecule \n'
        else:
            output += 'HITRAN molecule \n'
        return output
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        if not isinstance(value,str): raise TypeError('Molecule name should be string type')
        self._name=value
    
    @property
    def prodimo_name(self):
        return self._prodimo_name

    @prodimo_name.setter
    def prodimo_name(self,value):
        if not isinstance(value,str): raise TypeError('ProDiMo name should be string type')
        self._prodimo_name=value
        
    @property
    def iso(self):
        return self._iso

    @iso.setter
    def iso(self,value):
        try:
            value = int(value)
        except:
            pass
        if not (isinstance(value,np.int64) or isinstance(value,int)): raise TypeError('iso should be int or numpy.int64 type')
        self._iso=value
        
    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self,value):
        try:
            value = float(value)
        except:
            pass
        if not (isinstance(value,np.float64) or isinstance(value,float)): raise TypeError('mass should be float or numpy.float64 type')
        self._mass=value
        
    @property
    def waveSelection(self):
        return self._waveSelection

    @waveSelection.setter
    def waveSelection(self,value):
        self._waveSelection=value
        
    @property
    def ESelection(self):
        return self._ESelection

    @ESelection.setter
    def ESelection(self,value):
        self._ESelection=value
        
    @property
    def bandSelection(self):
        return self._bandSelection

    @bandSelection.setter
    def bandSelection(self,value):
        self._bandSelection=value
        
    @property
    def hitran_min_strength(self):
        return self._hitran_min_strength

    @hitran_min_strength.setter
    def hitran_min_strength(self,value):
        try:
            value = float(value)
        except:
            pass
        if not (isinstance(value,np.float64) or isinstance(value,float)): raise TypeError('Hitran minimum strength should be float or numpy.float64 type')
        self._hitran_min_strength=value
        
    @property
    def file(self):
        return self._file

    @file.setter
    def file(self,value):
        if not isinstance(value,str): raise TypeError('File path should be string type')
        self._file=value
        
    @property
    def custom_partition_sum(self):
        return self._custom_partition_sum

    @custom_partition_sum.setter
    def custom_partition_sum(self,value):
        if not isinstance(value,str): raise TypeError('custom_partition_sum path should be string type')
        self._custom_partition_sum=value
        
    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self,value):
        if not isinstance(value,str): raise TypeError('Output file path should be string type')
        self._output_file=value
        
    @property
    def custom(self):
        return self._custom

    @custom.setter
    def custom(self,value):
        if not isinstance(value,bool): raise TypeError('Custom is a bool type')
        self._custom=value
        
    @property
    def abundance_fraction(self):
        return self._abundance_fraction

    @abundance_fraction.setter
    def abundance_fraction(self,value):
        try:
            value = float(value)
        except:
            pass
        if not (isinstance(value,np.float64) or isinstance(value,float)): raise TypeError('abundance_fraction should be float or numpy.float64 type')
        self._abundance_fraction=value
        

def _conv_str(a):
    return(str(a))

def _conv_float(a):
    return float(a)

def _conv_int(a):
    return int(_conv_float(a))

_HITRANclassification2004 = {
                        'global':{
                            'diatomic':['CO','HF','HCl','HBr','HI','N2','NO+'],
                            'diatomicDiffElec':['O2'],
                            'diatomicDoubletPIElec':['NO','OH','ClO'],
                            'linearTriatomic':['N2O','OCS','HCN'],
                            'linearTriatomicLargeFermiResonance':['CO2'],
                            'nonlinearTriatomic':['H2O','O3','SO2','NO2','HOCl','H2S','HO2','HOBr'],
                            'linearTetratomic':['C2H2'],
                            'pyramidalTetratomic':['NH3','PH3'],
                            'nonlinearTetratomic':['H2CO','H2O2','COF2'],
                            'polyatomic':['CH4','CH3D','CH3Cl','C2H6','HNO3','SF6','HCOOH','ClONO2','C2H4','CH3OH']
                        },
                        'local':{
                            'asymmetricRotors':['H2O','O3','SO2','NO2','HNO3','H2CO','HOCl','H2O2','COF2','H2S','HO2','HCOOH','ClONO2','HOBr','C2H4'],
                            'diatomicORlinear':['CO2','N2O','CO','HF','HCl','HBr','HI','OCS','N2','HCN','C2H2','NO+'],
                            'sphericalRotors':['SF6','CH4'],
                            'symmetricRotors':['CH3D','CH3Cl','C2H6','NH3','PH3','CH3OH'],
                            'tripletSigmaGroundElec':['O2'],
                            'doubletPiGroundElec':['NO','OH','ClO']
                        }
                        }

_HITRANlevels2004 = {
                        'global':{
                            'diatomic':                          {'upper':[['NULL',13,_conv_str],['v1',2,_conv_int]],                                                                                                                             'lower':[['NULL',13,_conv_str],['v1*',2,_conv_int]]                                                                                                                                 },
                            'diatomicDiffElec':                  {'upper':[['NULL',12,_conv_str],['X',1,_conv_str],['v1',2,_conv_int]],                                                                                                            'lower':[['NULL',12,_conv_str],['X*',1,_conv_str],['v1*',2,_conv_int]]                                                                                                               },
                            'diatomicDoubletPIElec':             {'upper':[['NULL',7,_conv_str],['X',1,_conv_str],['i',3,_conv_str],['NULL',2,_conv_str],['v1',2,_conv_int]],                                                                        'lower':[['NULL',7,_conv_str],['X*',1,_conv_str],['i*',3,_conv_str],['NULL',2,_conv_str],['v1*',2,_conv_int]]                                                                          },
                            'linearTriatomic':                   {'upper':[['NULL',7,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int]],                                                                        'lower':[['NULL',7,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int]]                                                                         },
                            'linearTriatomicLargeFermiResonance':{'upper':[['NULL',6,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int],['r',1,_conv_int]],                                                       'lower':[['NULL',6,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int],['r*',1,_conv_int]]                                                       },
                            'nonlinearTriatomic':                {'upper':[['NULL',9,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int]],                                                                                          'lower':[['NULL',9,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                            },
                            'linearTetratomic':                  {'upper':[['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l',2,_conv_int],['pm',2,_conv_str],['r',2,_conv_int],['Sq',1,_conv_str]],     'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int], ['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l*',2,_conv_int],['pm*',2,_conv_str],['r*',2,_conv_int],['Sq*',1,_conv_str]]},
                            'pyramidalTetratomic':               {'upper':[['NULL',5,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['Sq',2,_conv_int]],                                                       'lower':[['NULL',5,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['Sq*',2,_conv_int]]                                                       },
                            'nonlinearTetratomic':               {'upper':[['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]],                                    'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                   },
                            'polyatomic':                        {'upper':[['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['n',2,_conv_str],['C',2,_conv_str]],                                      'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['n*',2,_conv_str],['C*',2,_conv_str]]                                     }
                        },
                        'local':{
                            'asymmetricRotors':      {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                      },
                            'diatomicORlinear':      {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                     },
                            'sphericalRotors':       {'upper':[['NULL',2,_conv_str],['J',3,_conv_int],['C',2,_conv_str],['alpha',3,_conv_int],['F',5,_conv_str]]             ,  'lower':[['NULL',2,_conv_str],['J*',3,_conv_int],['C*',2,_conv_str],['alpha*',3,_conv_int],['F*',5,_conv_str]]                                    },
                            'symmetricRotors':       {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['C',2,_conv_str],['Sym',1,_conv_str],['F',4,_conv_str]] ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['C*',2,_conv_str],['Sym*',1,_conv_str],['F*',4,_conv_str]]                      },
                            'tripletSigmaGroundElec':{'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',1,_conv_str],['Br*',1,_conv_str],['N*',3,_conv_int],['Br*',1,_conv_str],['J*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]},
                            'doubletPiGroundElec':   {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',3,_conv_str],['Br*',1,_conv_str],['J*',5,_conv_float],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                   }
                        }
                        }
_HITRANclassification2020 = {
                        'global':{
                            'diatomic_a':           ['CO','HF','HCl','HBr','HI','N2','NO+','H2','CS'],
                            'diatomic_b':           ['O2','NO','OH','ClO','SO'],
                            'linearTriatomic_a':    ['CO2'],
                            'linearTriatomic_b':    ['N2O','OCS','HCN','CS2'],
                            'nonlinearTriatomic':   ['H2O','O3','SO2','NO2','HOCl','H2S','HO2','HOBr'],
                            'pyramidalTetratomic_a':['NH3','PH3'],
                            'pyramidalTetratomic_b':['15NH3'],
                            'linearPolyatomic_a':   ['C2H2'],
                            'linearPolyatomic_b':   ['C4H2'],
                            'linearPolyatomic_c':   ['HC3N'],
                            'linearPolyatomic_d':   ['C2N2'],
                            'asymmetricTop_b':      ['H2O2'],
                            'asymmetricTop_a':      ['H2CO','H2O2','COF2'],
                            'planarSymmetric':      ['SO3'],
                            'sphericalTop':         ['CH4','13CH4','CF4','GeH4'],
                            'explicit':             ['CH3D','13CH3D','HNO3','CH3Cl','C2H6','CH3Br','SF6','HCOOH','ClONO2','C2H4','CH3OH','CH3CN','CH3F','CH3I']
                        },
                        'local':{
                            'asymmetricRotors_a':['H2O'],
                            'asymmetricRotors_b':['O3','SO2','HNO3','H2CO','HOCl','H2O2','COF2','H2S','HCOOH','ClONO2','HOBr','C2H4'],
                            'asymmetricRotors_c':['NO2','HO2'],
                            'closedShellDiatomicORlinear_a':['CO2','N2O','CO','HF','HCl','HBr','HI','OCS','HCN','C2H2','NO+','HC3N','CS','C2N2','CS2'],
                            'closedShellDiatomicORlinear_b':['C4H2'],
                            'closedShellDiatomicORlinear_c':['H2','N2'],
                            'sphericalRotors':['SF6','CH4','13CH4','CF6','GeH4'],
                            'symmetricRotors_a':['CH3D','13CH3D','15NH3','PH3','CH3OH','CH3CN','CH3Br','CH3Cl','CH3F','CH3I','NF3'],
                            'symmetricRotors_b':['NH3'],
                            'symmetricRotors_c':['C2H6'],
                            'planarSymmetric': ['SO3'],
                            'openShellDiatomicTripletSigmaGroundElec':['O2','SO'],
                            'openShellDiatomicDoubletPiGroundElec_a':['NO','ClO'],
                            'openShellDiatomicDoubletPiGroundElec_b':['OH']
                        }
                        }

_HITRANlevels2020 = {
                        'global':{
                            'diatomic_a':           {'upper': [['NULL',13,_conv_str],['v1',2,_conv_int]]                                                                                                                                                                                                                              ,'lower':[['NULL',13,_conv_str],['v1*',2,_conv_int]]                                                                                                                                                                                                                                      },
                            'diatomic_b':           {'upper': [['NULL',6,_conv_str],['X',2,_conv_str],['Omega',3,_conv_str],['NULL',3,_conv_str],['v1',2,_conv_int]]                                                                                                                                                                     ,'lower':[['NULL',6,_conv_str],['X*',2,_conv_str],['Omega*',3,_conv_str],['NULL',3,_conv_str],['v1*',2,_conv_int]]                                                                                                                                                                           },
                            'linearTriatomic_a':    {'upper': [['NULL',6,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int],['r',1,_conv_int]]                                                                                                                                                        ,'lower':[['NULL',6,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int],['r*',1,_conv_int]]                                                                                                                                                            },
                        'linearTriatomic_b':    {'upper': [['NULL',7,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int]]                                                                                                                                                                             ,'lower':[['NULL',7,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                                                                                                              },
                            'nonlinearTriatomic':   {'upper': [['NULL',9,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int]]                                                                                                                                                                                           ,'lower':[['NULL',9,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                                                                                                                                 },
                            'pyramidalTetratomic_a':{'upper': [['NULL',5,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['Sq',2,_conv_str]]                                                                                                                                                        ,'lower':[['NULL',5,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['Sq*',2,_conv_str]]                                                                                                                                                            },
                            'pyramidalTetratomic_b':{'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['NULL',1,_conv_str],['l3',1],['l4',1],['NULL',1,_conv_str],['l',1],['NULL',1,_conv_str],['gamma_rib',4,_conv_str]]                                                          ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['NULL',1,_conv_str],['l3*',1,_conv_int],['l4*',1,_conv_int],['NULL',1,_conv_str],['l*',1,_conv_int],['NULL',1,_conv_str],['gamma_rib*',4,_conv_str]]                                },
                            'linearPolyatomic_a':   {'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l4',2,_conv_int],['l5',2,_conv_int],['pm',1,_conv_str],['NULL',1,_conv_str],['Sq',1,_conv_str]]                                                            ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l4*',2,_conv_int],['l5*',2,_conv_int],['pm*',1,_conv_str],['NULL',1,_conv_str],['Sq*',1,_conv_str]]                                                            },
                            'linearPolyatomic_b':   {'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['v5',1,_conv_int],['v6',1,_conv_int],['v7',1,_conv_int],['v8',1,_conv_int],['v9',1,_conv_int],['NULL',1,_conv_str],['Sym',1,_conv_str],['NULL',1,_conv_str],['Sq',2,_conv_str]]   ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['v5*',1,_conv_int],['v6*',1,_conv_int],['v7*',1,_conv_int],['v8*',1,_conv_int],['v9*',1,_conv_int],['NULL',1,_conv_str],['Sym*',1,_conv_str],['NULL',1,_conv_str],['Sq*',2,_conv_str]] },
                            'linearPolyatomic_c':   {'upper': [['NULL',2,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['v5',1,_conv_int],['v6',1,_conv_int],['v7',1,_conv_int],['l5',2,_conv_int],['l6',2,_conv_int],['l7',2,_conv_int]]                                                             ,'lower':[['NULL',2,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['v5*',1,_conv_int],['v6*',1,_conv_int],['v7*',1,_conv_int],['l5*',2,_conv_int],['l6*',2,_conv_int],['l7*',2,_conv_int]]                                                            },
                            'linearPolyatomic_d':   {'upper': [['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l',2,_conv_int],['pm',1,_conv_str],['r',1,_conv_int],['Sq',1,_conv_str]]                                                                                                      ,'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l*',2,_conv_int],['pm*',1,_conv_str],['r*',1,_conv_str],['Sq*',1,_conv_str]]                                                                                                      },
                            'asymmetricTop_b':      {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]]                                                                                                                                     ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                                                                                                                        },
                            'asymmetricTop_a':      {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['n',1,_conv_int],['tau',1,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]]                                                                                                                   ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['n*',1,_conv_int],['tau*',1,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                                                                                                     },
                            'planarSymmetric':      {'upper': [['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['l3',2,_conv_int],['v4',2,_conv_int],['l4',2,_conv_int],['gamma_rib',3,_conv_str]]                                                                                                                                ,'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['l3*',2,_conv_int],['v4*',2,_conv_int],['l4*',2,_conv_int],['gamma_rib*',3,_conv_str]]                                                                                                                                  },
                            'sphericalTop':         {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['n',2,_conv_str],['Cg',2,_conv_str]]                                                                                                                                       ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['n*',2,_conv_str],['Cg*',2,_conv_str]]                                                                                                                                          },
                            'explicit':             {'upper': [['explicit',15,_conv_str]]                                                                                                                                                                                                                                            ,'lower':[['explicit*',15,_conv_str]]                                                                                                                                                                                                                                                    }
                        },
                        'local':{
                            'asymmetricRotors_a':                       {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['quad',1,_conv_str]]                                                    ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['quad*',1,_conv_str]]                                                                                 },
                            'asymmetricRotors_b':                       {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                                                     ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                                                                  },
                            'asymmetricRotors_c':                       {'upper':[['N',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                                                     ,  'lower':[['N*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                                                                  },
                            'closedShellDiatomicORlinear_a':            {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                                                                 },
                            'closedShellDiatomicORlinear_b':            {'upper':[['l6',2,_conv_str],['l7',2,_conv_str],['l8',2,_conv_str],['l9',2,_conv_str],['NULL',7,_conv_str]]                                                  ,  'lower':[['l6*',2,_conv_str],['l7*',2,_conv_str],['l8*',2,_conv_str],['l9*',2,_conv_str],['NULL',1,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['NULL',1,_conv_str]]   },
                            'closedShellDiatomicORlinear_c':            {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['mag-quad*',1,_conv_str],['F*',5,_conv_str]]                                                                            },
                            'sphericalRotors':                          {'upper':[['NULL',2,_conv_str],['J',3,_conv_int],['C',2,_conv_str],['alpha',3,_conv_int],['F',5,_conv_str]]                                                  ,  'lower':[['NULL',2,_conv_str],['J*',3,_conv_int],['C*',2,_conv_str],['alpha*',3,_conv_int],['F*',5,_conv_str]]                                                                                },
                            'symmetricRotors_a':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['C',2,_conv_str],['Sym',1,_conv_str],['F',4,_conv_str]]                                      ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['C*',2,_conv_str],['Sym*',1,_conv_str],['F*',4,_conv_str]]                                                                  },
                            'symmetricRotors_b':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['NULL',1,_conv_str],['gamma_rot',3,_conv_str],['gamma_rot2',3,_conv_str],['NULL',1,_conv_str]],  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['NULL',1],['gamma_rot*',3],['gamma_rot2*',3,_conv_str],['NULL',1,_conv_str]]                                               },
                            'symmetricRotors_c':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['Sym',3,_conv_str],['F',4,_conv_str]]                                                       ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['Sym*',3,_conv_str],['F*',4,_conv_str]]                                                                                    },
                            'planarSymmetric':                          {'upper':[['NULL',3,_conv_str],['J',3,_conv_int],['K',3,_conv_int],['NULL',2,_conv_str],['gamma_rot',3,_conv_str],['NULL',1,_conv_str]]                       ,  'lower':[['NULL',3,_conv_str],['J*',3,_conv_int],['K*',3,_conv_int],['NULL',2,_conv_str],['gamma_rot*',3,_conv_str],['NULL',1,_conv_str]]                                                      },
                            'openShellDiatomicTripletSigmaGroundElec':  {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                                                        ,  'lower':[['NULL',1,_conv_str],['Br*',1,_conv_str],['N*',3,_conv_int],['Br*',1,_conv_str],['J*',3,_conv_int],['F*',5,_conv_str],['M*',1,_conv_str]]                                              },
                            'openShellDiatomicDoubletPiGroundElec_a':   {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',2,_conv_str],['Br*',2,_conv_str],['J*',5,_conv_float],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                                                               },
                            'openShellDiatomicDoubletPiGroundElec_b':   {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                                                        ,  'lower':[['NULL',1,_conv_str],['Br*',2,_conv_str],['J*',5,_conv_float],['ul-Sym*',2,_conv_str],['F*',5,_conv_str]]                                                                            }
                        }
                        }
_HITRANformat = [2,1,12,10,10,5,5,10,4,8,15,15,15,15,6,12,1,7,7]
_HitranFMT = np.cumsum(_HITRANformat)
_HitranFMT = np.concatenate((np.array([0]),_HitranFMT))
_HITRANcolumns = ['Molecule_ID','Isotopologue_ID','nu','S','A','gamma_air','gamma_self','E_l','n_air','del_air','global_u','global_l','local_u','local_l','err_ind','References','line_mixing','g_u','g_l']


def _fetchLevelFormat(molecule='H2O',format:int=2020,verbose:bool=False):
    if format == 2020:
        HITRANclassification = _HITRANclassification2020
        HITRANlevels = _HITRANlevels2020
    else:
        HITRANclassification = _HITRANclassification2004
        HITRANlevels = _HITRANlevels2004
    A = list(HITRANclassification['global'].values())
    B = list(HITRANclassification['global'].keys())
    molGlobalType = None
    molLocalType = None
    for i in range(len(A)):
        if molecule in A[i]:
            molGlobalType = B[i]
            break
    A = list(HITRANclassification['local'].values())
    B = list(HITRANclassification['local'].keys())
    for i in range(len(A)):
        if molecule in A[i]:
            molLocalType = B[i]
            break
    if (molGlobalType is None) or (molLocalType is None):
        raise ValueError('Requested molecule does not exist in HITRAN classification to fetch quanta level formatting')
    if verbose:
        print('HITRAN classification for ',molecule, ' is: global quanta -',molGlobalType,', local quanta -',molLocalType)
    return HITRANlevels['global'][molGlobalType]['upper'],HITRANlevels['global'][molGlobalType]['lower'],HITRANlevels['local'][molLocalType]['upper'],HITRANlevels['local'][molLocalType]['lower']

def fetchLevelData(filePath,selectedMol='H2O',isotopologue=1,sortLabel=None,lowerLam=1,higherLam=30,format:int=2020,verbose:bool=False):
    globalUpper, globalLower, localUpper, localLower = _fetchLevelFormat(selectedMol,format=format,verbose=verbose)
    gbUfmt = [row[1] for row in globalUpper]
    gbUfmt_cum = np.concatenate((np.array([0]),np.cumsum(gbUfmt)))
    gbLfmt = [row[1] for row in globalLower]
    gbLfmt_cum = np.concatenate((np.array([0]),np.cumsum(gbLfmt)))
    locUfmt = [row[1] for row in localUpper]
    locUfmt_cum = np.concatenate((np.array([0]),np.cumsum(locUfmt)))
    locLfmt = [row[1] for row in localLower]
    locLfmt_cum = np.concatenate((np.array([0]),np.cumsum(locLfmt)))

    print('Molecule: ',selectedMol)
    print('Global upper quanta: ',[row[0] for row in globalUpper if row[0] != 'NULL'])
    print('Global lower quanta: ',[row[0] for row in globalLower if row[0] != 'NULL'])
    print('Local upper quanta: ',[row[0] for row in localUpper if row[0] != 'NULL'])
    print('Local lower quanta: ',[row[0] for row in localLower if row[0] != 'NULL'])

    gu = _HITRANcolumns.index('global_u')
    gl = _HITRANcolumns.index('global_l')
    lu = _HITRANcolumns.index('local_u')
    ll = _HITRANcolumns.index('local_l')

    globalU_d = []
    globalL_d = []
    localU_d = []
    localL_d = []
    lamb = []
    iso = []
    skippedCount = 0
    with open(filePath) as A:
        for i,Firstline in enumerate(A):
            global_u = Firstline[_HitranFMT[gu]:_HitranFMT[gu+1]]
            global_l = Firstline[_HitranFMT[gl]:_HitranFMT[gl+1]]
            local_u = Firstline[_HitranFMT[lu]:_HitranFMT[lu+1]]
            local_l = Firstline[_HitranFMT[ll]:_HitranFMT[ll+1]]
            globalU_d.append(global_u)
            globalL_d.append(global_l)
            localU_d.append(local_u)
            localL_d.append(local_l)
            lamb.append(1e4/_conv_float(Firstline[_HitranFMT[2]:_HitranFMT[3]]))
            iso.append(_conv_int(Firstline[_HitranFMT[1]:_HitranFMT[2]]))
        else:
            print('End of file read')
    
    globalU = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    globalL = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    localU  = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    localL  = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    
    for i in isotopologue:
        mask_gU = (globalU['Isotopologue_ID']==i) & (globalU['lambda']>lowerLam) & (globalU['lambda']<higherLam) # | (mask_gU) 
        mask_gL = (globalL['Isotopologue_ID']==i) & (globalL['lambda']>lowerLam) & (globalL['lambda']<higherLam) # | (mask_gL) 
        mask_lU = (localU['Isotopologue_ID']==i)  & (localU['lambda']>lowerLam)  & (localU['lambda']<higherLam)  # | (mask_lU) 
        mask_lL = (localL['Isotopologue_ID']==i)  & (localL['lambda']>lowerLam)  & (localL['lambda']<higherLam)  # | (mask_lL) 
    globalUreq  = globalU[mask_gU]
    globalLreq  = globalL[mask_gL]
    localUreq   = localU[mask_lU]
    localLreq   = localL[mask_lL]
    
    globalUd = list(compress(globalU_d, mask_gU))
    globalLd = list(compress(globalL_d, mask_gL))
    localUd = list(compress(localU_d, mask_lU))
    localLd = list(compress(localL_d, mask_lL))

    globalU_d = []
    globalL_d = []
    localU_d = []
    localL_d = []

    for i,(g_U,g_L,l_U,l_L) in enumerate(zip(globalUd,globalLd,localUd,localLd)):
        try:
            D = [i]+[row[2](g_U[gbUfmt_cum[j]:gbUfmt_cum[j+1]]) for j, row in enumerate(globalUpper)]
            E = [i]+[row[2](g_L[gbLfmt_cum[j]:gbLfmt_cum[j+1]]) for j, row in enumerate(globalLower)]
            F = [i]+[row[2](l_U[locUfmt_cum[j]:locUfmt_cum[j+1]]) for j, row in enumerate(localUpper)]
            G = [i]+[row[2](l_L[locLfmt_cum[j]:locLfmt_cum[j+1]]) for j, row in enumerate(localLower)]
            # print(D)
        except:
            skippedCount += 1
            continue
        try:
            globalU_d.append(D)
            globalL_d.append(E)
            localU_d.append(F)
            localL_d.append(G)
        except:
            warnings.warn('Line: '+str(i)+' Could not append quantum state and/or nu, iso')
    if skippedCount>0:
        warnings.warn(str(skippedCount)+' lines skipped due to mismatch in pharsing format and data')
    
    globalU = pd.DataFrame(globalU_d,columns=['num']+[rows[0] for rows in globalUpper])
    globalL = pd.DataFrame(globalL_d,columns=['num']+[rows[0] for rows in globalLower])
    localU = pd.DataFrame(localU_d,columns=['num']+[rows[0] for rows in localUpper])
    localL = pd.DataFrame(localL_d,columns=['num']+[rows[0] for rows in localLower])
    
    globalU  = globalU.drop(columns='NULL', errors='ignore')
    globalL  = globalL.drop(columns='NULL', errors='ignore')
    localU   =  localU.drop(columns='NULL', errors='ignore')
    localL   =  localL.drop(columns='NULL', errors='ignore')
    globalU.index = globalUreq.index
    globalL.index = globalLreq.index
    localU.index = localUreq.index
    localL.index = localLreq.index
    globalU = pd.concat([globalU,globalUreq],axis=1)
    globalL = pd.concat([globalL,globalLreq],axis=1)
    localU = pd.concat([localU,localUreq],axis=1)
    localL = pd.concat([localL,localLreq],axis=1)
    if sortLabel!=None:
        globalU = globalU.sort_values(sortLabel)
        globalL = globalL.sort_values(sortLabel)
        localU  = localU.sort_values(sortLabel)
        localL  = localL.sort_values(sortLabel)        
    return globalU,globalL,localU,localL

def read_hitran(filePath,moleculeName,isotopologue:list=[1],lowerLam=1,higherLam=30,sort_label='lambda',quanta=False,format:int=2020,verbose:bool=False):
    '''
    Returns the pandas dataframe containing HITRAN data of a given molecule
    
    Parameters
    ----------
    filePath : string
      HITRAN datafile path

    moleculeName : string
      Molecule name according to HITRAN format

    isotopologue : list
      list of integers corresponding to HITRAN isotopologue codes, e.g. [1,2] refers to the first and second most abundant isotopologues
    
    lowerLam : float
      Lower limit of wavelength
    
    higherLam : float
      Upper limit of wavelength
    
    sort_label: string
      DataFrame key to sort the output linedata 

    quanta: logical
      Whether to split the level notations into individual quantum numbers
    
    format : int
      Year format, 2020 or earlier
    
    verbose : logical
      More wordy output if True
    '''
    data = pd.read_fwf(filePath,widths=_HITRANformat,header=None, names=_HITRANcolumns)
    data['line_mixing']=data['line_mixing'].astype("boolean").fillna(False).astype(bool)
    mask = pd.Series([False]*len(data),dtype=bool)
    for i in isotopologue:
        mask = (mask) | (data['Isotopologue_ID']==i)
    mol = data[mask]
    mol.insert(2,'lambda',1e4/mol['nu'],True) #adding column wavelength in microns from freq in cm-1
    mol.insert(8,'E_u',mol['E_l']+mol['nu'],True)
    mol_MIR = mol[(mol['lambda']>lowerLam) & (mol['lambda']<higherLam)]
    mol_MIR.loc[mol_MIR['lambda']>0.0]['global_u'] = mol_MIR['global_u'].astype(str)
    mol_MIR.loc[mol_MIR['lambda']>0.0]['global_l'] = mol_MIR['global_l'].astype(str)
    mol_MIR.loc[mol_MIR['lambda']>0.0]['local_u'] = mol_MIR['local_u'].astype(str)
    mol_MIR.loc[mol_MIR['lambda']>0.0]['local_l'] = mol_MIR['local_l'].astype(str)
    if quanta:
        gu,gl,lu,ll = fetchLevelData(filePath,moleculeName,isotopologue=isotopologue,sortLabel=sort_label,lowerLam=lowerLam,higherLam=higherLam,format=format,verbose=verbose)
        gu = gu.drop(columns='Isotopologue_ID',  errors='ignore')
        gl = gl.drop(columns='Isotopologue_ID',  errors='ignore')
        lu = lu.drop(columns='Isotopologue_ID',  errors='ignore')
        ll = ll.drop(columns='Isotopologue_ID',  errors='ignore')
        
        gu = gu.drop(columns='num',  errors='ignore')
        gl = gl.drop(columns='num',  errors='ignore')
        lu = lu.drop(columns='num',  errors='ignore')
        ll = ll.drop(columns='num',  errors='ignore')
        
        mol_MIR = pd.merge(mol_MIR,gu, on='lambda')
        mol_MIR = pd.merge(mol_MIR,gl, on='lambda')
        mol_MIR = pd.merge(mol_MIR,lu, on='lambda')
        mol_MIR = pd.merge(mol_MIR,ll, on='lambda')
        mol_MIR = mol_MIR.drop(columns='global_u', errors='ignore')
        mol_MIR = mol_MIR.drop(columns='global_l', errors='ignore')
        mol_MIR = mol_MIR.drop(columns='local_u',  errors='ignore')
        mol_MIR = mol_MIR.drop(columns='local_l',  errors='ignore')
        return mol_MIR
    mol_MIR = mol_MIR.sort_values(sort_label)
    return mol_MIR

def getLevelFormat(molecule:str,format:int=2020,level:str='global'):
    '''
    Returns the HITRAN format of the ro-vibration levels of a molecule
    
    Parameters
    ----------
    molecule : string
      Molecule name according to HITRAN format
    
    format : int
      Year format, 2020 or earlier

    level : string: 'global' or 'local'
      'global' refers the vibration modes
      'local' refers to the rotation modes
    '''
    fmt = _fetchLevelFormat(molecule,format=format)
    if level=='global':
        j=0
    else:
        j=2
    myList = [i[0] for i in fmt[j]]
    valueToBeRemoved = 'NULL'

    try:
        while True:
            myList.remove(valueToBeRemoved)
    except ValueError:
        pass
    fmt = ''
    for i in myList:
        fmt = fmt+i+' '
    return(fmt)

def split_level_quant(line):
    '''
    Splits the level notation into individual qunatum numbers
    
    Parameters
    ----------
    line : string
      Level notation string
    '''
    if not isinstance(line,str): raise TypeError('The level quantum number definition should be a string')
    levels = ['','']
    ilvl = -1
    status = 'close'
    end = ''
    for i in range(len(line)):
        if status == 'close':
            if line[i] == '"':
                end = '"'
            elif line[i] == "'":
                end = "'"
        if line[i] == end:
            if status=='close':
                ilvl += 1
                status = 'open'
            else:
                status = 'close'
            continue
        if status == 'open':
            levels[ilvl] += line[i]
    return levels

def read_line_selection(path='./LineSelection.in'):
    '''
    Reads in the LineSelection.in formatted line selection data
    
    Parameters
    ----------
    path : string
      Path to the LineSelection.in file
    '''
    f = open(path,'r')
    lines = f.readlines()
    f.close()
    print('Reading line selection from ' + path)
    rules = []
    irule = -1
    i = 0
    maxL = len(lines)
    keep_going = True
    
    while keep_going:
        line = lines[i]
            
        if i>=maxL-1: keep_going = False
        
        if ('---' in line) or ('***' in line): 
            i += 1
            continue
            
        elif ('! name' in line) or ('! custom_molecule' in line):
            rules.append(selection_rules())
            irule += 1
            rules[irule].name = line.split()[0]
            if '! name' in line:
                rules[irule].custom == False
            else:
                rules[irule].custom == True
            
        elif '! iso' in line:
            rules[irule].iso = int(float(line.split()[0]))
            
        elif '! mass' in line:
            rules[irule].mass = float(line.split()[0])
            
        elif '! abundance_fraction' in line:
            rules[irule].abundance_fraction = float(line.split()[0])
            
        elif '! waveSelection' in line:
            line = int(line.split()[0])
            rules[irule].waveSelection = []
            for j in range(line):
                lin = lines[i+j+1]
                rules[irule].waveSelection.append([float(k) for k in lin.split()])
            i = i+line
            
        elif '! ESelection' in line:
            line = int(line.split()[0])
            rules[irule].ESelection = []
            for j in range(line):
                lin = lines[i+j+1]
                rules[irule].ESelection.append([float(k) for k in lin.split()])
            i = i+line
            
        elif '! bandSelection' in line:
            line = int(line.split()[0])
            rules[irule].bandSelection = []
            for j in range(line):
                lin = lines[i+j+1]
                rules[irule].bandSelection.append(split_level_quant(lin))
            i = i+line
            
        elif '! hitran_min_strength' in line:
            rules[irule].hitran_min_strength = float(line.split()[0])
            
        elif '! file' in line:
            rules[irule].file = line.split()[0].replace("'","").replace('"','')
            
        elif '! output_file' in line:
            rules[irule].output_file = line.split()[0].replace("'","").replace('"','')
            
        elif '! prodimo_name' in line:
            rules[irule].prodimo_name = line.split()[0].replace("'","").replace('"','')
            
        elif '! custom_partition_sum' in line:
            rules[irule].custom_partition_sum = line.split()[0].replace("'","").replace('"','')
            
        i += 1
    return rules

def read_hitran_from_rules(rule,year=2020):
    '''
    Reads in hitran data provided a 'selection_rule' object
    '''
    if not isinstance(rule,selection_rules): raise TypeError('rule should be an instance of class prodimopy.hitran.selection_rules')
    wmin,wmax = 0,1e99
    if not rule.waveSelection is None:
        wmin = np.amin([wmin,np.amin(rule.waveSelection)])
        wmax = np.amax([wmax,np.amax(rule.waveSelection)])
    if rule.iso is None: rule.iso = 1
    if rule.file is None: raise ValueError('File path should be given in the LineSelectionPP.in, cannot be blank')
    if rule.name is None: raise ValueError('Molecule name should be given in the LineSelectionPP.in, cannot be blank')
    data = read_hitran(filePath      = rule.file,
                    moleculeName = (rule.name).split('_')[0],
                    isotopologue = [rule.iso],
                    lowerLam     = wmin, 
                    higherLam    = wmax, 
                    sort_label   = 'E_u', 
                    quanta       = False, 
                    format       = year, 
                    verbose      = False)
    
    mask = (data['nu']>0) & (data['A']>0)
    if not rule.waveSelection is None:
        wmask = data['nu']<0
        for i in range(len(rule.waveSelection)):
            wmask = wmask | ((data['lambda']>np.amin(rule.waveSelection[i])) & (data['lambda']<np.amax(rule.waveSelection[i])))
        mask = mask & wmask
    
    if not rule.ESelection is None:
        emask = data['nu']<0
        for i in range(len(rule.ESelection)):
            emask = emask | ((data['E_u']>np.amin(rule.ESelection[i])/(c*h/k*1e2)) & (data['E_u']<np.amax(rule.ESelection[i])/(c*h/k*1e2)))
        mask = mask & emask
    
    if not rule.bandSelection is None:
        bmask = data['nu']<0
        for i in range(len(rule.bandSelection)):
            bmask = bmask | (((rule.bandSelection[i][0] == data['global_u']) & (rule.bandSelection[i][1] == data['global_l'])) | ((rule.bandSelection[i][0] == data['global_l']) & (rule.bandSelection[i][1] == data['global_u'])))
        mask = mask & bmask
    
    if not rule.hitran_min_strength is None:
        mask = mask & (data['A']*data['g_u']*np.exp(-data['E_u']*(c*h/k*1e2)/1500)>rule.hitran_min_strength)
    
    return data[mask]

def create_lamda_line_level(dat):
    '''
    Ceates ordered line and level data from HITRAN data as required for LAMDA format
    '''
    NLINE = len(dat)
    lvldata = np.zeros((1,1,NLINE*2,4))
    lvldata[0,0,:NLINE,0] = dat['E_u']
    lvldata[0,0,:NLINE,1] = dat['g_u']
    lvldata[0,0,NLINE:,0] = dat['E_l']
    lvldata[0,0,NLINE:,1] = dat['g_l']
    lvldata[0,0,:NLINE,2] = np.linspace(1,NLINE,NLINE,dtype=int)
    lvldata[0,0,NLINE:,2] = np.linspace(1,NLINE,NLINE,dtype=int)
    lvldata[0,0,:,:] = lvldata[0,0,lvldata[0,0,:, 0].argsort(),:]
    lvldata[0,0,:,3] = np.linspace(1,NLINE*2,NLINE*2,dtype=int)
    dat = dat.reset_index()
    dat['ind'] = np.linspace(0,NLINE-1,NLINE,dtype=int)
    linedat = dat.sort_values(by='nu',ascending=True)
    return linedat,lvldata

def write_lamda_file(linedat,lvldata,molecule,mol_weight,filename):
    '''
    Writes LAMDA formatted file containing ordered line and level data
    '''
    NLINE = len(linedat)
    NLEVEL = len(lvldata[0,0,:,0])
    f = open(filename,'w')
    text = ['!MOLECULE\n',f' {molecule}\n','!MOLECULAR WEIGHT\n',f'{mol_weight:7.1f}\n','!NUMBER OF ENERGY LEVELS\n',f'{NLEVEL:9d}\n','!LEVEL + ENERGIES(cm^-1) + WEIGHT\n']
    for D in lvldata[0,0,:,:]:
        text.append(f'{int(D[-1]):6d}{D[0]:12.4f}{D[1]:7.1f}  "Nan"\n')
    text.append('!NUMBER OF RADIATIVE TRANSITIONS\n')
    text.append(f'{NLINE:8d}\n')
    text.append('!TRANS + UP + LOW + EINSTEINA(s^-1) + FREQ(GHz) + E_u(K)\n')
    for i,D in enumerate(np.array(linedat['ind']).tolist()):
        A = lvldata[0,0,np.argwhere(lvldata[0,0,:,2]==D+1),3]
        text.append(f'{i+1:8d}{int(A.T[0][1]):7d}{int(A.T[0][0]):7d}{np.array(linedat["A"])[i]:11.3e}{np.array(linedat["nu"]*(c*1e-7))[i]:18.7f}{np.array(linedat["E_u"])[i]*c*h/k*1e2:12.2f}\n')
    text.append('!NUMBER OF COLL PARTNERS\n')
    text.append('0\n')
    f.writelines(text)
    f.close()
    print('Written '+filename)
    return
