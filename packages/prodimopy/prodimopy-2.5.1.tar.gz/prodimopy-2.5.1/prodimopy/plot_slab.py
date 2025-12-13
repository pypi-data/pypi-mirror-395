"""
.. module:: plot_slab
   :synopsis: Plot routines for prodimo slab models.

.. moduleauthor:: A. M. Arabhavi


"""


import numpy as np
import pandas as pd
from scipy.constants import h,c,k
from adjustText import adjust_text
import matplotlib.pyplot as plt
from prodimopy.read_slab import slab_data,slab,slab1D,generate_grid
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import spectres
sci_c = c*1.00

class default_figsize:
    def __init__(self):
        self.width = 7
        self.height = 5

defFigSize = default_figsize()

def set_default_figsize(w=defFigSize.width,h=defFigSize.height):
    defFigSize.width,defFigSize.height = w,h
    return
def _get_set_fig(ax=None,fig=None,figsize=None):
    if ax is None:
        if fig is None:
            figg,axx = plt.subplots(figsize=(defFigSize.width,defFigSize.height))
        else:
            figg = fig
            axx = fig.add_subplot()
    else:
        if fig is None:
            figg = ax.get_figure()
            axx = ax
        else:
            axx = ax
            figg = fig
            fig2 = ax.get_figure()
            if fig2!=fig:
                print('WARNING, passed figure and axis do not match')
                fig = ax.get_figure()
    if figsize != None:
        figg.set_size_inches(figsize[0], figsize[1], forward=True)
    return(figg,axx)

def plotBoltzmannDiagram(dat,ax=None,fig=None,figsize=None,NLTE=False,label=None,s=0.1,c='k',set_axis_limits=True):
    """
    This function plots the Boltzmann diagram (reduced flux vs upper energy level)
    """
    fig,ax = _get_set_fig(ax,fig,figsize)
    data_list = []
    label_list = []
    s_list = []
    c_list = []
    if isinstance(dat,slab):
        data_list.append(dat)
        label_list.append(label)
        s_list.append(s)
        c_list.append(c)
    elif isinstance(dat,list) or isinstance(dat,slab_data):
        if isinstance(dat,slab_data): 
            data_list = dat.models
        else:
            data_list = dat
        if isinstance(label,list):
            label_list = label
        elif isinstance(label,str):
            for i in range(len(data_list)):
                label_list.append(label)
        elif isinstance(label,type(None)):
            for i in range(len(data_list)):
                label_list.append('')
        if isinstance(s,list):
            s_list = label
        elif isinstance(s,float) or isinstance(s,int):
            for i in range(len(data_list)):
                s_list.append(s)
        if isinstance(c,list):
            c_list = c
        elif isinstance(c,str):
            for i in range(len(data_list)):
                c_list.append(c)
    else:
        raise ValueError('The data passed should be of type "slab" or a list containing "slab"s ')
    max_Eu,min_Eu = 1e-99,1e99
    max_F,min_F = 1e-99,1e99
    FTag = 'FLTE'
    if NLTE:
        FTag = 'FNLTE'
    for i,Dat in enumerate(data_list):
        F  = Dat.linedata[FTag]
        nu = Dat.linedata['GHz']
        A  = Dat.linedata['A']
        gu = Dat.linedata['gu']
        Eu = Dat.linedata['Eu']
        RedF = F/(nu*A*gu*1e9)
        max_Eu = np.amax([np.amax(Eu),          max_Eu])
        max_F  = np.amax([np.amax(RedF),        max_F])
        min_Eu = np.amin([np.amin(Eu),          min_Eu])
        min_F  = np.amin([np.amin(RedF[RedF>0]),min_F])
        ax.scatter(Eu,RedF,s=s_list[i],label=label_list[i],c=c_list[i])
    if not(label_list[0] is None):
        ax.legend()
    ax.set_yscale('log')
    if set_axis_limits:
        ax.set_xlim([min_Eu*0.9,max_Eu*1.02])
        ax.set_ylim([min_F*10**-0.5,max_F*10**0.5])
    ax.set_xlabel('Eu')
    ax.set_ylabel(r'$F/(\nu A g_u)$')
#         print([np.amin(RedF[RedF>0])*0.9,np.amax(RedF)*1.02])
#         print([np.amin(RedF[RedF>0])*10**-0.5,np.amax(RedF)*10**0.5])
    return(fig,ax)

def plotLevelDiagram(data,ax=None,figsize=(10,18),seed=None,lambda_0=None,lambda_n=None,width_nlines=False):
    """
    This function plots level diagram for a single slab model
    """
    
    if(seed==None):
        seed = np.random.randint(0,2**25-1)
    np.random.seed(seed)
    try:
        lineData = data.linedata
        levData = data.leveldata
    except:
        levData = data[0]
        lineData = data[1]
    if lambda_0!=None:
        reqLineData = lineData[c/lineData['GHz']*1e-3>lambda_0]
        lineData = reqLineData
    if lambda_n!=None:
        reqLineData = lineData[c/lineData['GHz']*1e-3<lambda_n]
        lineData = reqLineData
    levData = levData.set_index('i')
    lineData = lineData.set_index('i')
    
    selU = np.asarray(list(set(lineData['u'])))
    selL = np.asarray(list(set(lineData['l'])))
    selGU = np.asarray(list(set(lineData['global_u'])))
    selGL = np.asarray(list(set(lineData['global_l'])))
    
    levArr= []
    for i in selGU:
        selLines = lineData[lineData['global_u']==i]
        lev= np.amin(levData.loc[selLines['u']]['E'])
        levArr.append([i,lev])

    for i in selGL:
        selLines = lineData[lineData['global_l']==i]
        lev= np.amin(levData.loc[selLines['l']]['E'])
        levArr.append([i,lev])
        
    levArr = pd.DataFrame(levArr,columns=['Level','E']).drop_duplicates().sort_values(by=['E'])
    linArr = pd.DataFrame([lineData['global_u'],lineData['global_l']]).transpose().drop_duplicates()
    levArr['err'] = np.random.uniform(0.05,0.95,len(levArr))
    
    text = []
    if ax==None:
        fig,ax = plt.subplots(figsize=figsize)
    else:
        ax = plt.gca()
        fig = ax.get_figure()
    for i in range(len(levArr['E'])):
        ax.axhline(y=levArr.iloc[i]['E'],xmin=levArr.iloc[i]['err']-0.05,xmax=levArr.iloc[i]['err']+0.05,color='k')
        t = ax.text(levArr.iloc[i]['err'],levArr.iloc[i]['E'],levArr.iloc[i]['Level'])
        text.append(t)
    widths = []
    for i in range(len(linArr)):
        gu = linArr.iloc[i]['global_u']
        gl = linArr.iloc[i]['global_l']
        widths.append(np.sum(lineData[(lineData['global_u']==gu)&(lineData['global_l']==gl)]['FLTE']))
    widths=np.array(widths)/np.amax(widths)
    if width_nlines:
        widths = []
        for i in range(len(linArr)):
            gu = linArr.iloc[i]['global_u']
            gl = linArr.iloc[i]['global_l']
            widths.append(len(lineData[(lineData['global_u']==gu)&(lineData['global_l']==gl)]['FLTE']))
        widths=np.array(widths)/np.amax(widths)        
    for i in range(len(linArr)):
        gu = linArr.iloc[i]['global_u']
        gl = linArr.iloc[i]['global_l']
        yu = levArr[levArr['Level']==gu]['E']
        yl = levArr[levArr['Level']==gl]['E']
        eu = levArr[levArr['Level']==gu]['err']
        el = levArr[levArr['Level']==gl]['err']
        ax.plot([el.iloc[0],eu.iloc[0]],[yl.iloc[0],yu.iloc[0]],lw=widths[i]*2.5+0.1)
    
    ax.set_xlim([0,1])
    adjust_text(text)
    ax.set_ylabel('Energy (K)')
    ax.axes.xaxis.set_ticklabels([])
    ax.tick_params(top=False,bottom=False)
    
    print('Random seed = ',seed)
    return(fig,ax,seed)

def plot_lines(dat, normalise = False, fig=None, ax=None, overplot=False, c=None, cmap=None, colors=None, figsize=None, NLTE=False, label='', lw=1, scaling=1,offset=0):
    """
    This function plots total line fluxes (erg/s/cm2/sr)
    """
    if isinstance(dat,slab_data):
        dat = dat.models
    elif isinstance(dat,slab):
        dat = [dat]
    elif isinstance(dat,list):
        pass
    else:
        raise ValueError('Wrong input slab data')
    color_list = []
    fig_list = []
    ax_list = []
    offset_list = []
    scaling_list = []
    label_list = []
    if isinstance(label,list):
        label_list = label
    else:
        for i in range(len(dat)):
            if label=='': 
                label_list.append(i)
            else:
                label_list.append(label)
    if c is None: c='k'
                
    if isinstance(offset,float) or isinstance(offset,int):
        for i in range(len(dat)):
            offset_list.append(offset*(i+1))
    elif isinstance(offset,list):
        offset_list = offset
    elif isinstance(offset,np.ndarray):
        offset_list.append(offset)
    else:
        raise ValueError('offset takes only int, float or list of int or float or numpy array')

    
    if isinstance(scaling,float) or isinstance(scaling,int):
        for i in range(len(dat)):
            scaling_list.append(scaling)
    elif isinstance(scaling,list):
        scaling_list = scaling
    else:
        raise ValueError('scaling takes only int, float or list of int or float')
    
    if cmap is None: cmap = 'jet'
    values = range(len(dat))
    jet = cmm = plt.get_cmap(cmap) 
    cNorm  = mcolors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=jet)

    if overplot:
        fig,ax = _get_set_fig(ax,fig,figsize)
        values = range(len(dat))
        fig_list.append(fig)
        ax_list.append(ax)
        for i in range(len(dat)):
            color_list.append(scalarMap.to_rgba(i))
    else:
        try:
            if len(ax)>1: axx_len = len(ax)
        except:
            axx_len = 1
        if axx_len>1:
            for i in range(axx_len):
                figg,axx = _get_set_fig(ax[i],fig,figsize)
                ax_list.append(axx)
                fig_list.append(figg)
                color_list.append(c)
                # for i in range(len(ax)): fig_list.append(fi)
        else:
            for i in range(len(dat)):
                figg,axx = _get_set_fig(ax,fig,figsize)
                fig_list.append(figg)
                ax_list.append(axx)
                color_list.append(scalarMap.to_rgba(i))
    if not (colors is None) and isinstance(colors,list):
        if len(colors) == len(color_list):
            color_list = colors.copy()

    if overplot:
        for i,slb in enumerate(dat):
            if NLTE:
                t = 'FNLTE'
            else:
                t = 'FLTE'
            fig,ax = _basic_line_plot(sci_c/slb.linedata['GHz']*1e-3, slb.linedata[t], scaling=scaling_list[i], normalise=normalise, fig=fig_list[0], ax=ax_list[0], figsize=figsize, label=label_list[i], color=color_list[i], lw=lw,offset=offset_list[i])
        return(fig,ax)
    else:
        for i,slb in enumerate(dat):
            if NLTE:
                t = 'FNLTE'
            else:
                t = 'FLTE'
            fig_list[i],ax_list[i] = _basic_line_plot(sci_c/slb.linedata['GHz']*1e-3, slb.linedata[t], scaling=scaling_list[i], normalise=normalise, fig=fig_list[i], ax=ax_list[i], figsize=figsize, label=label_list[i], color=color_list[i], lw=lw,offset=offset_list[i])
        if axx_len>1:
            return(fig_list[0],np.array(ax_list))
        else:
            return([(fig,ax) for (fig,ax) in zip(fig_list,ax_list)])
        
        
def _basic_line_plot(x,y,normalise=False,fig=None, ax=None, scaling=1, figsize=None, label='', color='k', lw=1,offset = 0.0):
    # fig,ax = _get_set_fig(ax,fig,figsize)
    if x is None or y is None:
        raise ValueError('x or y is None')
    if normalise:
        y = y/np.amax(y)
    ax.vlines(x, 0.0+offset, y*scaling+offset, label = label, color=color, lw=lw)
    ax.set_xlabel('Wavelength [microns]')
    ax.legend()
    return(fig,ax)


def plot_spectra(dat, normalise = False, fig=None, ax=None, overplot=False, add=False, cmap=None, colors=None, style='step', figsize=None, NLTE=False, label='', lw=1, c=None, scaling=1, sampling=None, offset=0, overlap=False, custom_wave=None):
    """
    This function plots convolved spectra (erg/s/cm2/sr)
    """

    if isinstance(dat,slab_data):
        dat = dat.models
    elif isinstance(dat,slab):
        dat = [dat]
    elif isinstance(dat,list):
        pass
    else:
        raise ValueError('Wrong input slab data')
    color_list = []
    fig_list = []
    ax_list = []
    offset_list = []
    scaling_list = []
    label_list = []
    if isinstance(label,list):
        label_list = label
    else:
        for i in range(len(dat)):
            if label=='': 
                label_list.append(i)
            else:
                label_list.append(label)
    if c is None: c='k'
                
    if isinstance(offset,float) or isinstance(offset,int):
        for i in range(len(dat)):
            offset_list.append(offset*(i+1))
    elif isinstance(offset,list):
        offset_list = offset
    elif isinstance(offset,np.ndarray):
        offset_list.append(offset)
    else:
        raise ValueError('offset takes only int, float or list of int or float or numpy array')

    
    if isinstance(scaling,float) or isinstance(scaling,int):
        for i in range(len(dat)):
            scaling_list.append(scaling)
    elif isinstance(scaling,list):
        scaling_list = scaling
    else:
        raise ValueError('scaling takes only int, float or list of int or float')
    
    
    if cmap is None: cmap = 'jet'
    values = range(len(dat))
    jet = cmm = plt.get_cmap(cmap) 
    cNorm  = mcolors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=jet)   
    
    for d in dat:
        if not overlap:
            if d.convWavelength is None:
                raise ValueError('The model is not convolved, please use .convolve() method')
        else:
            if d.convOverlapFreq is None:
                raise ValueError('The model is not convolved, please use .convolve_overlap() method')
        
    if not overlap:
        add_wave = dat[0].convWavelength
        add_flux = add_wave*0.0
    else:
        add_wave = sci_c/dat[0].convOverlapFreq*1e-3
        add_flux = add_wave*0.0
    if add:
        if not overlap:
            for i,d in enumerate(dat):
                if not np.array_equal(add_wave, d.convWavelength):
                    raise ValueError('Convolved wavelength grid not same for molecules within a model')
            if NLTE:
                for i,d in enumerate(dat):
                    add_flux+=d.convNLTEflux
            else:
                for i,d in enumerate(dat):
                    add_flux+=d.convLTEflux
            convRR = dat[0].convR
        else:
            for i,d in enumerate(dat):
                if not np.array_equal(add_wave, d.convOverlapFreq):
                    raise ValueError('Convolved wavelength grid not same for molecules within a model')
            if NLTE:
                for i,d in enumerate(dat):
                    add_flux+=d.convOverlapNLTE
            else:
                for i,d in enumerate(dat):
                    add_flux+=d.convOverlapLTE
            convRR = dat[0].convOverlapR
        fig,ax = _get_set_fig(ax,fig,figsize)
        fig,ax = _basic_spectra_plot(add_wave, add_flux,convR = convRR, sampling=sampling, scaling=scaling, normalise=normalise, fig=fig, ax=ax, style=style, figsize=figsize, label=label, color=c,lw=lw, where='mid',offset=offset,custom_wave=custom_wave)
        return(fig,ax)
    
    if overplot:
        fig,ax = _get_set_fig(ax,fig,figsize)
        values = range(len(dat))
        if cmap is None: cmap = 'jet'
        jet = cmm = plt.get_cmap(cmap) 
        cNorm  = mcolors.Normalize(vmin=0, vmax=values[-1])
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=jet)
        fig_list.append(fig)
        ax_list.append(ax)
        for i in range(len(dat)):
            color_list.append(scalarMap.to_rgba(i))
    else:
        try:
            if len(ax)>1: axx_len = len(ax)
        except:
            axx_len = 1
        if axx_len>1:
            for i in range(axx_len):
                figg,axx = _get_set_fig(ax[i],fig,figsize)
                ax_list.append(axx)
                fig_list.append(figg)
                color_list.append(c)
                # for i in range(len(ax)): fig_list.append(fi)
        else:
            for i in range(len(dat)):
                figg,axx = _get_set_fig(ax,fig,figsize)
                fig_list.append(figg)
                ax_list.append(axx)
                color_list.append(scalarMap.to_rgba(i))
    if not (colors is None) and isinstance(colors,list):
        if len(colors) == len(color_list):
            color_list = colors.copy()
            
    if overplot:
        for i,d in enumerate(dat):
            if not overlap:
                add_wave = d.convWavelength
                if NLTE:
                    add_flux=d.convNLTEflux
                else:
                    add_flux=d.convLTEflux
                convRR = dat[i].convR
            else:
                add_wave = sci_c/d.convOverlapFreq*1e-3
                if NLTE:
                    add_flux=d.convOverlapNLTE
                else:
                    add_flux=d.convOverlapLTE
                convRR = dat[i].convOverlapR
            fig_list[0],ax_list[0] = _basic_spectra_plot(add_wave, add_flux,convR= convRR,sampling=sampling, scaling=scaling_list[i], offset=offset_list[i],  normalise=normalise, fig=fig_list[0], ax=ax_list[0], style=style, figsize=figsize, label=label_list[i], color=color_list[i],lw=lw, where='mid',custom_wave=custom_wave)
        return(fig_list[0],ax_list[0])
    else:
        for i,d in enumerate(dat):
            if not overlap:
                add_wave = d.convWavelength
                if NLTE:
                    add_flux=d.convNLTEflux
                else:
                    add_flux=d.convLTEflux
                convRR = dat[i].convR
            else:
                add_wave = sci_c/d.convOverlapFreq*1e-3
                if NLTE:
                    add_flux=d.convOverlapNLTE
                else:
                    add_flux=d.convOverlapLTE
                convRR = dat[i].convOverlapR
            fig_list[i],ax_list[i] = _basic_spectra_plot(add_wave, add_flux,convR= convRR,sampling=sampling, scaling=scaling_list[i], offset=offset_list[i],  normalise=normalise, fig=fig_list[i], ax=ax_list[i], style=style, figsize=figsize, label=label_list[i], color=color_list[i],lw=lw, where='mid',custom_wave=custom_wave)
        if axx_len>1:
            return(fig_list[0],np.array(ax_list))
        else:
            return([(fig,ax) for (fig,ax) in zip(fig_list,ax_list)])
            
def plot_1D_spectra(dat, convolved = False, R=None, normalise = False, fig=None, ax=None, style='step', figsize=None, label='', lw=1, c=None, scaling=1, sampling=None, offset=0,custom_wave=None):
    """
    This function plots spectra of 1D slab models (erg/s/cm2/sr)
    """

    if not isinstance(dat,slab1D):
        raise ValueError('Wrong input 1D slab data')

    if ((not convolved) or (dat.convWavelength is None)) and (R is None):
        Flux = dat.flux
        Wavelength = sci_c/dat.frequency*1e-3
        convR = dat.R
    elif not (R is None):
        tempFlux = dat.conv_flux
        temp_R = dat.convR
        temp_Freq = dat.convFrequency
        temp_Wave = dat.convWavelength
        dat.convolve(R=R,verbose=False)
        Flux = dat.flux
        Wavelength = sci_c/dat.frequency*1e-3
        convR = R
        dat.conv_flux = tempFlux
        dat.convR = temp_R
        dat.convFrequency = temp_Freq
        dat.convWavelength = temp_Wave
    elif not ((not convolved) or (dat.convWavelength is None)):
        Flux = dat.conv_flux
        Wavelength = dat.convWavelength
        convR = dat.convR
    else:
        raise ValueError('The model is not convolved, please set convolved=False or use .convolve() method or specify a resolving power to plot')

    Flux = Flux[np.argsort(Wavelength)]
    Wavelength = Wavelength[np.argsort(Wavelength)]
    fig,ax = _get_set_fig(ax,fig,figsize)
    fig,ax = _basic_spectra_plot(Wavelength, Flux,convR = convR, sampling=sampling, scaling=scaling, normalise=normalise, fig=fig, ax=ax, style=style, figsize=figsize, label=label, color=c,lw=lw, where='mid',offset=offset,custom_wave=custom_wave)
    return(fig,ax)

def plot_1D_structure(dat, figsize=None,grid_point=False):
    """
    This function plots structure of 1D slab models
    """
    fig,ax = plt.subplots(1,5,figsize=figsize,sharey=True)
    if grid_point:
        x_array = [i+1 for i in range(dat.Ngrid)]
        ax[0].set_xlabel('Grid points (i)')
    else:
        x_array = np.cumsum(dat.grid['dz'])
        ax[0].set_xlabel('z [au]')
    ax[0].plot(dat.grid['dz'],   x_array,c='k')
    ax[0].set_xlabel('dz')
    ax[0].set_xscale('log')
    
    ax[1].plot(dat.grid['vturb'],x_array,c='k')
    ax[1].set_xlabel('v$_{turb}$ [km/s]')

    ax[2].plot(dat.grid['nd'],   x_array,c='k')
    ax[2].set_xlabel('n$_d$ [cm$-3$]')
    ax[2].set_xscale('log')
    
    ax[3].plot(dat.grid['Td'],   x_array,c='k')
    for i in range(dat.Nspecies): 
        ax[3].plot(dat.grid['Tg_'+dat.species[i]],x_array,c=cm.viridis(i/dat.Nspecies),ls='solid',label=dat.species[i])
    ax[3].set_xlabel('T [K]')
    ax[3].legend(loc='upper left')
    
    array = dat.grid['nH2']+dat.grid['nHI']+dat.grid['nHII']+dat.grid['nHe']+dat.grid['nelec']
    for i in range(dat.Nspecies):
        array += dat.grid['n'+dat.species[i]]
    ax[4].plot(array,x_array,c='k')
    ax[4].plot(dat.grid['nH2'],x_array,c='r',ls='solid',label='nH2')
    ax[4].plot(dat.grid['nHI'],x_array,c='r',ls='dashed',label='nHI')
    ax[4].plot(dat.grid['nHII'],x_array,c='r',ls='dotted',label='nHII')
    ax[4].plot(dat.grid['nHe'],x_array,c='r',ls='dashdot',label='nHe')
    ax[4].plot(dat.grid['nelec'],x_array,c='r',ls=(0, (3, 1, 1, 1, 1, 1)),label='nelec')
    for i in range(dat.Nspecies): 
        ax[4].plot(dat.grid['n'+dat.species[i]],x_array,c=cm.viridis(i/dat.Nspecies),ls='solid',label=dat.species[i])
    ax[4].legend(loc='upper left')
    ax[4].set_xscale('log')
    ax[4].set_xlabel('n [cm$^-3$]')

    

    return(fig,ax)
        
def _basic_spectra_plot(x, y, convR,sampling=None,normalise=False, fig=None, ax=None, scaling=1, offset=0.0, figsize=None, label='', color='k', style='step', lw=1, where='post', R=1e6,custom_wave=None):
    if x is None or y is None:
        raise ValueError('x or y is None, mostly the data is not convolved. Please use .convolve() method first')
    fig,ax = _get_set_fig(ax,fig,figsize)
    if normalise:
        y = y/np.amax(y)
    y = y*scaling+offset
    if not custom_wave is None:
        y = spectres.spectres(custom_wave,x,y, verbose=False,fill=0.0)
        x = custom_wave*1.0
    if not sampling is None:
        x_new = sci_c/generate_grid(R=convR,lambda_0=np.amin(x),lambda_n=np.amax(x),sampling=sampling)*1e-3
        y = spectres.spectres(x_new,x,y, verbose=False,fill=0.0)
        x = x_new*1.0
    if style=='step':
        ax.step(x, y, lw=lw, label = label, color=color, where=where)
    else:
        ax.plot(x, y, lw=lw, label = label, color=color)
    ax.set_xlabel('Wavelength [microns]')
    # ax.legend()
    return(fig,ax)