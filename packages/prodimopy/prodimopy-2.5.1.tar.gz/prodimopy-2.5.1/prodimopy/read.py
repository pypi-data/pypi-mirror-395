"""
.. module:: read
   :synopsis: Reads the output data of a |prodimo| model and stores it in a data structure.

.. moduleauthor:: Ch. Rab

"""

import cProfile
from collections import OrderedDict
from collections.abc import MutableMapping
import typing
import glob
import math
import os
from timeit import default_timer as timer
import warnings

# for now use type_extensions to be compatible with python < 3.13
from typing_extensions import deprecated, TypeAlias

from astropy import constants as const
from astropy import units as u
from scipy.interpolate import interp1d
import scipy.integrate as integrate
import f90nml as nml
from tqdm import tqdm


import numpy as np
from numpy.typing import NDArray
import prodimopy.chemistry.network as pcnet

# This activates deprecation warnings, otherwise they are not seen (from e.g. numpy)
warnings.filterwarnings("default", category=DeprecationWarning)

# Type Alias for the 2D grid fields, is just for typing
TGridfloat: TypeAlias = np.ndarray[tuple[int, int], np.float64]


def _do_cprofile(func):
    """
    Simple profiling

    Taken from here: https://zapier.com/engineering/profiling-python-boss/

    Can be used via a decorator: i.e. place '@do_cprofile' before the method you want to profile.
    But please also remove it again after profiling.
    """

    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort="time")

    return profiled_func


class DataStar(object):
    """
    Stellar spectrum and several stellar properties.

    This object holds data from `StarSpectrum.out` but also from other sources such as `ProDiMo.out`.

    It also provides some convenience functions for e.g. `Lstar` or the mass accretion rate derived from the UV luminosity.

    """

    def __init__(self, nlam, teff, r, logg, luv):
        """

        Constructor for reading StarSpectrum.out.
        Other properties are filled later, if possible.

        Attributes
        ----------

        """
        self.nlam: int = nlam
        """ : number of wavelength points """
        self.teff: float = teff
        r""" : effective temperature *Unit*: :math:`\mathrm{K}` """
        self.r: float = r
        r""" : radius *Unit*: :math:`\mathrm{R_\odot}` """
        self.logg: float = logg
        r""" : surface gravity *Unit*: :math:`\mathrm{cm/s^2}` """
        self.lam: NDArray[np.float64] = np.zeros(shape=(nlam))
        r""" : Stellar specturm wavelength *Unit*: :math:`\mathrm{\mu m}` """
        self.nu: NDArray[np.float64] = np.zeros(shape=(nlam))
        r""" : Stellar specturm frequency *Unit*: :math:`\mathrm{Hz}` """
        self.Inu: NDArray[np.float64] = np.zeros(shape=(nlam))
        r""" : Stellar Spectrum intensity *Unit*: :math:`\mathrm{erg/cm^2/s/Hz/sr}` """
        self.InuBand: NDArray[np.float64] | None = None
        r""" : Stellar Spectrum band averaged (from RTinterpolation.out) *Unit*: :math:`\mathrm{erg/cm^2/s/Hz/sr}` """
        self.InuInterpol: NDArray[np.float64] | None = None
        r""" : Stellar Spectrum interpolated (J_NU_FROM_RT, from RTinterpolation.out) *Unit*: :math:`\mathrm{erg/cm^2/s/Hz/sr}` """
        self.wlInterpol: NDArray[np.float64] | None = None
        r""" : wl grid for the interpolated specturm is in micron. """
        self.mass: float | None = None
        r""" : stellar mass *Unit*: :math:`\mathrm{M_\odot}` """
        self.Lstar: float | None = None
        r""" : stellar luminosity (from ProDiMo.out) *Unit*: :math:`\mathrm{L_\odot}`. Does not include accretion luminosity. """        
        self._Rsun=6.959900000e10  # from ProDiMo init_nature.f
        self._Lsun=3.846000000E+33 # from ProDiMo init_nature.f
        self._Msun=1.988922500E+33 # from ProDiMo init_nature.f
        self._lambs: NDArray[np.float64] | None = None # just to hold the band wl, if RTinterpolation.out can be read

    @property
    def lumAccr(self):
        r""": The accretion luminosity *Unit*: :math:`\mathrm{erg/s}`

        Is the excess luminosity :math:`L_\mathrm{accr}` due to accretion, i.e. the part that is added to the pure stellar photosphere spectrum (i.e. no accretion).
        We consider here only the part of the spectrum with :math:`\lambda \geq 0.0912` micron.

        .. math::

            L_\mathrm{accr}=L(\lambda \geq 0.0912\,\mathrm{micron}) - L_\mathrm{star}


        Where :math:`L_\mathrm{star}` is the value from `Parameter.in` (read from `ProDiMo.out`),
        and :math:`L` is the total luminosity for :math:`\lambda \geq 0.0912` micron.

        """
        lumtot = self.calcLum(lammin=0.0912)
        return lumtot - (self.Lstar * self._Lsun)

    @property
    def mdot(self):
        r""": The mass accretion rate in :math:`\mathrm{M_\odot/yr}` derived from the UV luminosity.

        Uses:

        .. math::

            L_\mathrm{accr} = G \times M_{*} \times \dot{M}_\mathrm{accr} / R

        where we use :attr:`lumAccr` for :math:`L_\mathrm{accr}`.

        """

        Rstar = self.r * self._Rsun
        Laccr = self.lumAccr
        Mstar = self.mass * self._Msun
        Maccr = Rstar * Laccr / (const.G.cgs.value * Mstar)

        return ((Maccr * u.g / u.s).to(u.Msun / u.yr)).value

    @property
    def lumTot(self):
        """: The total stellar luminosity (full spectrum) *Unit*: erg/s"""
        return self.calcLum()

    @property
    def lum(self):
        r""": The "stellar" luminosity :math:`(\lambda \geq 0.0912 \, \mathrm{\mu m})` *Unit*: :math:`\mathrm{erg/s}`

        This includes the accretion component if present.
        """
        return self.calcLum(lammin=0.0912)

    @property
    def lumEUV(self):
        """: stellar EUV luminosity *Unit*: erg/s

        Defined as everything with energies between and 13.6 eV and 100 eV.
        """

        lammin = ((0.0999999 * u.keV).to(u.micron, equivalencies=u.spectral())).value
        lammax = 0.0911999999
        return self.calcLum(lammin=lammin, lammax=lammax)

    @property
    def lumXray(self):
        """: stellar X-ray luminosity *Unit*: erg/s

        The luminosity for the part of the spectrum with energies >= 0.1 keV.
        """
        lammax = ((0.1 * u.keV).to(u.micron, equivalencies=u.spectral())).value
        return self.calcLum(lammax=lammax)

    def calcLum(self, lammin: float | None = None, lammax: float | None = None) -> float:
        """
        Integrates the stellar spectrum from `lammin` to `lammax` and returns the luminosity.

        Parameters
        ----------
        lammin :
            minimum wavelength in micron. Default: `None` (i.e. first wavelength point)

        lammax :
            maximum wavelength in micron. Default: `None` (i.e. last wavelength point)

        Returns
        -------
        float
            The luminosity from `lammin` to `lammax` in `erg/s`

        """
        # Set default wavelength limits
        if lammin is None:
            lammin = self.lam[0]
        if lammax is None:
            lammax = self.lam[-1]

        # Create mask for wavelength range
        mask = (self.lam >= lammin) & (self.lam <= lammax)

        # Integrate Inu over frequency
        # Inu is in erg/cm²/s/Hz/sr, need to integrate over frequency
        # additional pi for because it is /pi
        # *-1.0 because nu is in descending order
        lum_erg_per_s = (
            integrate.trapezoid(self.Inu[mask], x=self.nu[mask])
            * -1.0
            * 4.0
            * math.pi**2
            * (self.r * self._Rsun) ** 2
        )  # surface area

        return lum_erg_per_s

    def __str__(self):
        return (
            f"Mstar: {self.mass:g} Msun"
            + "\n"
            + f"Rstar: {self.r:g} Rsun"
            + "\n"
            + f"Teff:  {self.teff:g} K"
            + "\n"
            + f"Lstar: {self.Lstar:g} Lsun"
            + "\n"
            + f"L:     {self.lum / self._Lsun:g} Lsun"
            + "\n"
            + f"Ltot:  {self.lumTot / self._Lsun:g} Lsun"
            + "\n"
            + f"Laccr: {self.lumAccr / self._Lsun:g} Lsun"
            + "\n"
            + f"LEUV:  {self.lumEUV:g} erg/s"
            + "\n"
            + f"LXray: {self.lumXray:g} erg/s"
            + "\n"
            + f"Mdot:  {self.mdot:g} Msun/yr"
        )


class DataContinuumObs(object):
    """
    Holds the observational data for the continuum (the dust).

    Holds the photometric data, spectra (experimental) and radial profiles
    (experimental).

    .. todo::

      - proper documentation

    """

    def __init__(self, nlam=None):
        if nlam is not None:
            self.nlam = nlam
            self.lam = np.zeros(shape=(nlam))
            self.nu = np.zeros(shape=(nlam))
            self.fnuErg = np.zeros(shape=(nlam))
            self.fnuJy = np.zeros(shape=(nlam))
            self.fnuErgErr = np.zeros(shape=(nlam))
            self.fnuJyErr = np.zeros(shape=(nlam))
            self.flag = np.empty(nlam, dtype="U2")
        else:
            self.nlam = None
            self.lam = None
            self.nu = None
            self.fnuErg = None
            self.fnuJy = None
            self.fnuErgErr = None
            self.fnuJyErr = None
            self.flag = None

        self.specs = None
        """ holds a list of spectra if available (wl,flux,error) """
        self.R_V = None
        self.E_BV = None
        self.A_V = None

        self.radprofiles = None


class DataContinuumImages(object):
    """
    Holds the continuum images (image.out) and provides a method to read
    one particular image.

    The coordinates x,y are the same for all images, and only stored once.

    .. todo::

      - find a better solution for the multiple inclinations (Problem: don't want to read through the whole file).
    """

    def __init__(self, nlam, nx, ny, incl=None, filepath="./image.out"):
        """

        Attributes
        ----------

        """
        self.nlam: int = nlam
        """ : The number of wavelength points (== number of images) """
        self.lams: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The wavelengths. *UNIT:* micron, *DIMS:* (nlam) """
        self.nx: int = nx
        """ : The number of x axis points (radial) of the image """
        self.ny: int = ny
        """ : The number of y axis points (or theta) of the image """
        self.x: NDArray[np.float64] = np.zeros(shape=(nx, ny))
        """ : x coordinates. *UNIT:* au, *DIMS:* (nx,ny) """
        self.y: NDArray[np.float64] = np.zeros(shape=(nx, ny))
        """ : y coordinates. *UNIT:* au, *DIMS:* (nx,ny) """
        self._filepath = filepath
        self._inclinations = list()
        self._incidx = 0  # which inclination to use
        self._x=list()
        self._y=list()

    @property
    def inclination(self):
        return self._inclinations[self._incidx]

    def __str__(self):
        output = "ny: " + str(self.nx) + " nx: " + str(self.ny) + " nlam: " + str(self.nlam)
        output += " incl: " + str(self.inclination)
        return output

    def getImage(self, wl: float, iinc: int = 0) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64],float]:
        """
        Reads the intensities at a certain wavelength (image) from the image.out
        file.

        The image with the closest wavelength to the given wavelength (wl) will be
        returned.

        Parameters
        ----------
        wl : float
          the wavelength in micron of the requested image

        iinc : int
          the inclination index in case of multiple inclinations. Default ``iinc=0``

        Returns
        -------
        tuple : 
          x, y coordinates DIM(nx,ny), intensities DIM(nx,ny), UNIT: erg/cm^2/s/Hz/sr, and the exact wavelength Unit: micron
        """
        idx = np.argmin(np.abs(self.lams - wl))

        # jump to the inclination requested, but check first
        if iinc < 0 or iinc >= len(self._inclinations):
            raise ValueError("iinc must be between 0 and " + str(len(self._inclinations) - 1))

        # also set the current inclination 
        self._incidx=iinc

        skiprows = 6 * (iinc + 1) + (self.nx * self.ny) * iinc

        # first time need to init _x,_y
        if len(self._x)==0 or len(self._y)==0:
            self._x=[None]*len(self._inclinations)
            self._y=[None]*len(self._inclinations)
            
        # read the coordinates only once
        # ix,iz, x, y ... not required here
        if self._x[iinc] is None or self._y[iinc] is None:
            xy = np.loadtxt(self._filepath, skiprows=skiprows, usecols=(2, 3), max_rows=self.nx * self.ny)
            x = xy[:, 0].reshape(self.nx, self.ny)
            y = xy[:, 1].reshape(self.nx, self.ny)
            self._x[iinc]=x
            self._y[iinc]=y
        else:
            # FIXME: no so great, but avoids reading the file again
            x=self._x[iinc]
            y=self._y[iinc]

        intens = np.loadtxt(
            self._filepath, skiprows=skiprows, usecols=4 + int(idx), max_rows=self.nx * self.ny
        )

        return x,y,intens.reshape((self.nx, self.ny)), self.lams[idx]


class DataSEDAna(object):
    """
    Holds the analysis data for the Spectral Energy Distribution (SEDana.out).
    """

    def __init__(self, nlam: int, nx: int):
        """
        Initializes the SED analysis data.

        Parameters
        ----------
        nlam :
          The number of wavelength points.
        nx :
          The number of radial points.

        Attributes
        ----------
        """
        self.lams = np.zeros(shape=(nlam))
        """ Wavelength points `shape=(nlam)` """
        self.r15 = np.zeros(shape=(nlam))
        """ The r15 radius (when 15% of the emission are reached. `shape=(nlam)` """
        self.r85 = np.zeros(shape=(nlam))
        """ The r85 radius (when 85% of the emission are reached. `shape=(nlam)` """
        self.z15 = np.zeros(shape=(nlam, nx))
        """ The z15 height for each radial grid point (when 15% of the emission are reached from the top). `shape=(nlam,nx)` """
        self.z85 = np.zeros(shape=(nlam, nx))
        """ The z85 height for each radial grid point (when 85% of the emission are reached from the top). `shape=(nlam,nx)` """


class DataSED(object):
    """
    Holds the data for the Spectral Energy Distribution (SED).

    In case of multiple inclinations the data for all inclinations is stored.
    One can select a SED for a given inclination via :func:`~prodimopy.Data_ProDiMo.sedinc`
    """

    def __init__(self, nlam: int, distance: float):
        """
        Parameters
        ----------
        nlam :
          The number of wavelength points.

        distance :
          The distance of the target in pc.

        Attributes
        ----------
        """
        self.nlam: int = nlam
        """ : number of wavelength points """
        self.distance: float = distance
        """ : distance for which the SED was calculated. UNIT: pc """
        self.lam: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : the wavelength points in micron DIM: nlam """
        self.nu: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : the frequency points in Hz DIM: nlam """
        self.sedAna: DataSEDAna | None = None
        """ : the SED analysis data. Holds the data for the emission origin """
        # the quantities that hold the data for all inclinations
        self._fnuErgs: list[np.float64] = list()
        self._nuFnuWs: list[np.float64] = list()
        self._fnuJys: list[np.float64] = list()
        self._inclinations: list[np.float64] = list()
        self._Lbols: list[np.float64] = list()
        self._Tbols: list[np.float64] = list()
        self._incidx: int = 0

    def __str__(self):
        text = str(self.nlam) + "/" + str(self.inclination) + "/" + str(self.distance) + "/" + "\n"
        text = text + str(self._inclinations)
        return text

    @property
    def fnuErg(self) -> np.float64:
        """: The flux density `nuF_nu` in erg/s/cm^2, without extinction."""
        return self._fnuErgs[self._incidx]

    @property
    def nuFnuW(self) -> np.float64:
        """: The flux density `nuF_nu` in W/m^2; without extinction."""
        return self._nuFnuWs[self._incidx]

    @property
    def fnuJy(self) -> np.float64:
        """: The flux density in Jy; without extinction."""
        return self._fnuJys[self._incidx]

    @property
    def inclination(self) -> np.float64:
        """: The current inclination. See :func:`prodimopy.read.sedinc`."""
        return self._inclinations[self._incidx]

    @property
    def Lbol(self) -> np.float64:
        """: The bolometric luminosity in `L_sun`. See :func:`setLbolTbol`."""
        return self._Lbols[self._incidx]

    @property
    def Tbol(self) -> np.float64:
        """: The bolometric temperature in K. See :func:`setLbolTbol`."""
        return self._Tbols[self._incidx]

    def setLbolTbol(self):
        """
        Calculates the bolometric temperature and luminosity for the given
        values of the SED. Quite approximate at the moment.

        .. todo::

          - check the correctness of the calculation
          - provide a proper reference for the procedure we follow.
          - allow for more flexibility
        """

        # FIXME: correctness needs to be verified
        # calculate the bolometric luminosity
        # *-1.0 because of the ordering of nu
        # calculate Tbol see Dunham 2008 Equation 6
        # check what is here the proper value
        # in particular Tbol is very sensitive to this value
        # Lbol does not seem to change much (e.g. if 0.1 is used instead)
        # for the moment exclude the shortest wavelength as these is most likely scattering
        mask = self.lam > 0.2

        self._Lbols[self._incidx] = integrate.trapezoid(self.fnuErg[mask], x=self.nu[mask]) * -1.0
        self._Lbols[self._incidx] = (
            self.Lbol * 4.0 * math.pi * (((self.distance * u.pc).to(u.cm)).value) ** 2
        )
        self._Lbols[self._incidx] = self.Lbol / (const.L_sun.cgs).value

        self._Tbols[self._incidx] = (
            1.25e-11
            * integrate.trapezoid((self.nu[mask] * self.fnuErg[mask]), x=self.nu[mask])
            / integrate.trapezoid(self.fnuErg[mask], x=self.nu[mask])
        )

    def extinction(self, sedObs: DataContinuumObs, extmodel: str = "F99") -> NDArray[np.float64]:
        """
        Return the extinction for the given model.

        .. note::
          Please cite https://joss.theoj.org/papers/10.21105/joss.07023
          if you use this function in your work.

        Parameters
        ----------

        sedObs :
          The observed data for the continuum. Needs the R_V and E_BV values.

        extmodel :
          The model to use for the extinction. Default: "F99"
          For supported models see `astropy dust_extinction <https://dust-extinction.readthedocs.io/en/stable/dust_extinction/choose_model.html#parameter-dependent-average-curves>`_

        Returns
        -------
          : The extinction values for the given model. `shape=(nlam)` E.g. do `flux*extinction(model.sedObs)`.
        """
        import dust_extinction.parameter_averages as extmodels

        if sedObs is None:
            raise ValueError("No sedObs data for the extinction available.")

        tmpm = getattr(extmodels, extmodel.upper(), None)
        if tmpm is None:
            raise ValueError("Extinction model not supported: " + extmodel.upper())

        print("INFO: Applying extinction model:", extmodel)

        extm = tmpm(sedObs.R_V)
        ext = np.ones(self.lam.shape)
        ist = np.argmin(np.abs(self.lam - 1.0 / extm.x_range[1]))
        ien = np.argmin(np.abs(self.lam - 1.0 / extm.x_range[0]))

        ext[ist:ien] = extm.extinguish(self.lam[ist:ien] * u.micron, Ebv=sedObs.E_BV)
        return ext


class DataLineEstimate(object):
    """
    Data container for a single line estimate.

    This includes also the radial information (e.g. line emitting region).
    However, this data is only read on demand.

    """

    def __init__(self, ident: str, wl: float, jup: int, jlow: int, flux: float):
        """
        Attributes
        ----------

        """
        self.ident: str = ident
        """ The line identification (species name) """
        self.wl: float = wl
        """ The wavelength of the line in ``micron`` """
        self.jup: int = jup
        """ Upper level as defined in |prodimo| (not necessarily the real one!) """
        self.jlow: int = jlow
        """ Lower level as defined in |prodimo| (not necessarily the real one!). """
        self.flux: float = flux
        """ The integrated line flux in ``W/m^2`` """
        self.rInfo: list[DataLineEstimateRInfo] | None = None
        """ The extra radial information (i.e. info about the line emitting region). """
        self.__posrInfo = None
        """ stores the position of the radial information to access is later on """

    @property
    def frequency(self) -> float:
        """: Frequency of the line in ``GHz``."""
        return (self.wl * u.micrometer).to(u.GHz, equivalencies=u.spectral()).value

    @property
    def flux_Jy(self) -> float:
        """: The flux of the line in [Jansky km |s^-1|]."""
        return _flux_Wm2toJykms(self.flux, self.frequency)
    
    def luminosityErgs(self, distance: float) -> float:
        """
        Returns the luminosity in erg/s for the given distance
        
        simply calls :func:`~prodimopy.read.DataLineEstimate.luminosityWatt` and converts the result to erg/s.
        """
        return ((self.luminosityWatt(distance) * u.Watt).to(u.erg / u.s)).value

    def luminosityWatt(self, distance: float) -> float:
        """
        Parameters
        ----------
        distance : float
          The distance in pc, to calculate the line luminosity.
        
        Returns
        -------
        float
            Returns the line luminosity in Watt
                        
        """
        return (4.0 * math.pi * (distance * u.pc).to(u.m) ** 2 * self.flux * u.Watt / u.m**2).value

    def __str__(self):
        return f"LineEst: {self.ident:16} wl={self.wl:13.6f} μm  flux={self.flux:10.3e} W/m^2  (up={self.jup:5} low={self.jlow:5})"


class DataLineEstimateRInfo(object):
    """
    Data container for the extra radial information for a single line estimate.
    The data is read from `FlineEstimates.out`.
    This object corresponds to one line of the radial information in `FlineEstimates.out`
    """

    def __init__(self, ix, iz, Fcolumn, tauLine, tauDust, z15, z85, ztauD1, Ncol):
        """

        Attributes
        ----------

        """
        self.ix: int = ix
        """ : The x-coordinate index. """
        self.iz: int = iz
        """ : The z-coordinate index. """
        self.Fcolumn: float = Fcolumn
        """ : the line flux in the particular column (check again, i guess the iz coordinate is irrelevant for that) """
        self.tauLine: float = tauLine
        """ : the total vertical optical depth of the line measured from tauDust=1 upwards f(r) """
        self.tauDust: float = tauDust
        """ : the total vertical optical depth of the dust at the wl of the line as f(r) """
        self.z15: float = z15
        """ : z-level where the line flux reaches 15% of the total flux as f(r) (integrated from top to bottom of the disk); *UNIT:* au """
        self.z85: float = z85
        """ : z-level where the line flux reaches 85% as f(r) (integrated from top to bottom of the disk); *UNIT:* au """
        self.ztauD1: float = ztauD1
        """ : z-level where `taudust_ver(lambda_line)=1`; *UNIT:* au
            Is `None` for FlineEstimates version < 3
        """
        self.Ncol: float = Ncol
        """ : The column density of the species as f(r) measured from `ztauD1` upwards; UNIT: |cm^-2|
            It considers both halves of the disks (i.e. for the case of tauDust <1 ) so the values can be different to
            :attr:`~prodimopy.read.Data_ProDiMo.cdnmol` where only one half of the disk is considered.
            Is `None` for FlineEstimates version < 3
        """


class DataLineProfile:
    """
    Data container for a spectral line profile for a single spectral line.

    Attributes
    ----------

    """

    def __init__(self, nvelo, restfrequency=None):
        self.nvelo: int = nvelo
        """ : number of velocity points of the profile. """
        self.restfrequency: float = restfrequency
        """ : the restfrequency of the line. Useful for conversions. Optional. *UNIT:* GHz """
        self.velo: NDArray[np.float64] = np.zeros(shape=(self.nvelo))
        """ : The velocity grid of the line profile. *UNIT:* kms/s, *DIMS:* (nvelo) """
        self._flux = np.zeros(shape=(self.nvelo))
        self._flux_dust = np.zeros(shape=(self.nvelo))
        self._flux_conv = np.zeros(shape=(self.nvelo))
        self._flux_unit = "Jy"

    def __flux_unitconv(self, flux):
        """Internal function to convert the flux to the correct unit."""
        if self.flux_unit == "ErgAng":
            return (
                (flux * u.Jy)
                .to(
                    u.erg / u.s / u.cm**2 / u.angstrom,
                    equivalencies=u.spectral_density(self.restfrequency * u.GHz),
                )
                .value
            )
        elif self.flux_unit == "mJy":
            return flux * 1000.0
        else:
            return flux

    @property
    def flux(self) -> NDArray[np.float64]:
        """: The flux at each velocity point. *UNIT:* given by :attr:`flux_unit`, *DIMS:* (nvelo)"""
        return self.__flux_unitconv(self._flux)

    @flux.setter
    def flux(self, val):
        self._flux = val

    @property
    def flux_dust(self) -> NDArray[np.float64]:
        """: The flux of the dust (continuum) at each velocity point. *UNIT:* given by :attr:`flux_unit`, DIMS: (nvelo)"""
        return self.__flux_unitconv(self._flux_dust)

    @flux_dust.setter
    def flux_dust(self, val):
        self._flux_dust = val

    @property
    def flux_conv(self) -> NDArray[np.float64]:
        """: The flux at each velocity point for the convolved spectrum. UNIT: given by :attr:`flux_unit`, DIMS: (nvelo)"""
        return self.__flux_unitconv(self._flux_conv)

    @flux_conv.setter
    def flux_conv(self, val):
        self._flux_conv = val

    @property
    def frequency(self) -> float:
        """: The frequencies according to the velocity grid. Is relative to the restfrequency. UNIT: GHz
        FIXME: restfreq can be None ...
        """
        return (
            (self.velo * u.km / u.s)
            .to(u.GHz, equivalencies=u.doppler_optical(self.restfrequency * u.GHz))
            .value
        )

    @property
    @deprecated("Use flux_unit instead")
    def fluxErgAng(self):
        """
        The fluxes in units of erg/s/cm^2/Angstrom.

        .. deprecated:: 2.4.0
          Use :attr:`flux_unit` instead.
        """
        return (
            (self._flux * u.Jy)
            .to(
                u.erg / u.s / u.cm**2 / u.angstrom,
                equivalencies=u.spectral_density(self.restfrequency * u.GHz),
            )
            .value
        )

    @property
    def flux_unit(self) -> str:
        """: The flux unit for the line profile (e.g. for plotting).
        Possible choices: ``Jy`` (default), ``mJy`` and ``ErgAng``.
        """
        return self._flux_unit

    @flux_unit.setter
    def flux_unit(self, val: str):
        if val != "Jy" and val != "mJy" and val != "ErgAng":
            raise ValueError(f"flux unit {val} not supported")
        self._flux_unit = val

    def convolve(self, R):
        """
        Convolves the given profile to the spectral resolution R.
        The profile is convolved with a Gaussian where R determines the FWHM of that
        Gaussian. The results are stored in :attr:`flux_conv`

        Parameters
        ----------
        R :
            The spectral resolution.


        Returns
        -------
        float :
          The FWHM of the Gaussian in units of `km/s` i.e. the spectral resolution.
        """

        facFWHM = 2.355  # for getting the FWHM of a gaussian (i.e. stddev to FWHM

        if R is None or R <= 0.0:
            self._flux_conv = self._flux
            return

        delta_v = (const.c / R).to(u.km / u.s).value
        delta_v = delta_v / facFWHM  # need stdv for the  gaussian but R is interpreted as the FWHM

        gaussian = np.exp(-((self.velo) ** 2.0) / (2.0 * delta_v**2.0))

        # FIXME: Does not work if the continuum is not removed
        # also the 0 might not be the continuum
        flux = self._flux[:] - self._flux[0]

        norm = integrate.trapezoid(flux, self.velo)
        flux_convolved = np.convolve(flux, gaussian, "same")
        flux_convolved *= norm / integrate.trapezoid(flux_convolved, self.velo)

        self._flux_conv = flux_convolved + self._flux[0]
        return delta_v * facFWHM

    def __str__(self):
        return "nvelo: " + str(self.nvelo)


class DataLine(object):
    """
    Data container for a single spectral line read from `line_flux.out`.

    All lines can then be accessed via `model.lines`, where model is a :class:`~prodimopy.read.Data_ProDiMo` object.
    To print a decent looking list of all lines (in the notebook or console) one can use the following code:

    .. code-block:: python

      print(*model.lines,sep="\\n")

    This works also with a list of lines selected via :func:`~prodimopy.read.Data_ProDiMo.selectLines`:.
    But of course a simple for loop will also do the trick.


    Attributes
    ----------

    """

    def __init__(self):
        self.wl: float = 0.0
        """ : Rest-wavelength of the line. UNIT: `micron` """
        self.frequency: float = 0.0
        """ : Rest-frequency of the line. UNIT: `GHz` """
        self.prodimoInf: str = ""
        """ : Some information String from |prodimo| (i.e. transition) """
        self.species: str = ""
        """ : The chemical species of the line. Derived from ident. """
        self.ident: str = ""
        """ : The identification of the line (i.e. as given in `LineTransferList.in`) """
        self.distance: float | None = None
        """ : The distance used for the line calculations. UNIT: pc """
        self._fluxs: list[float] = list()
        """ : The integrated line flux. UNIT: W/m^2 """
        self._fconts: list[float] = list()
        """ : The continuum flux at the line position. UNIT: Jy """
        self._profiles: list[DataLineProfile] = list()
        """ : The line profile(s) for this particular line for each inclination. """
        self._inclinations: list[float] = list()
        """ : The list of inclinations to use for the line calculations. UNIT: deg """
        self._incidx: int = 0
        """ : The current inclination index to use. """

    @property
    def flux(self) -> float:
        """: The integrated line flux for the current inclination. UNIT: W/m^2"""
        return self._fluxs[self._incidx]

    @property
    def fcont(self) -> float:
        """: The continuum flux at the line position for the current inclination. UNIT: Jy"""
        return self._fconts[self._incidx]

    @property
    def profile(self) -> list[DataLineProfile]:
        """: The line profile(s) for this particular line for each inclination."""
        return self._profiles[self._incidx]

    @property
    def inclination(self) -> float:
        """: The current inclination. Unit: degrees."""
        return self._inclinations[self._incidx]

    @property
    def flux_Jy(self) -> float:
        """: The flux of the line in Jansky km |s^-1|."""
        return _flux_Wm2toJykms(self.flux, self.frequency)

    @property
    def fcontErgAng(self) -> float:
        """: The flux of the continuum in erg/s/cm^2/Angstrom"""
        return (
            (self.fcont * u.Jy)
            .to(
                u.erg / u.s / u.cm**2 / u.angstrom,
                equivalencies=u.spectral_density(self.frequency * u.GHz),
            )
            .value
        )

    @property
    def luminosityErgs(self):
        """: Returns the luminosity in erg/s"""
        return ((self.luminosityWatt * u.Watt).to(u.erg / u.s)).value

    @property
    def luminosityWatt(self):
        """: Returns the line luminosity in Watt"""
        return (
            4.0 * math.pi * (self.distance * u.pc).to(u.m) ** 2 * self.flux * u.Watt / u.m**2
        ).value

    @property
    def FWHM(self) -> float:
        """
        Calculate the Full Width at Half Maximum (FWHM) of a flux profile.

        This method computes the FWHM by finding the velocity range where the flux
        is above half of the maximum value. The calculation searches for the leftmost
        and rightmost points where the flux crosses the half-maximum threshold.

        Parameters
        ----------

        convolved : bool
            If True, the FWHM is calculated from the convolved flux profile.

        Returns
        -------
        float
            The FWHM in km/s, calculated as the difference between the
            right and left velocity values at half maximum (vright - vleft).

        Notes
        -----
        - The half maximum is calculated as the average of the maximum and minimum
          flux values: 0.5 * (max(flux) + min(flux)) , so the continuum is taken care off
        - The left boundary search starts from index 0 and stops when flux exceeds
          half maximum or reaches the end of the array
        - The right boundary search starts from the last index and stops when flux
          exceeds half maximum, or reaches index 0
        - The method assumes that vright > vleft in the velocity profile

        """
        return self._FWHM(convolved=False)

    @property
    def FWHM_convolved(self) -> float:
        """
        Calculate the Full Width at Half Maximum (FWHM) of a convolved flux profile.
        For details see :func:`FWHM`
        """
        return self._FWHM(convolved=True)

    def _FWHM(self, convolved: bool = False) -> float:
        """
        Just a helper routine, so that one can still use the property decorator
        """

        if convolved:
            flux_profile = self.profile.flux_conv
        else:
            flux_profile = self.profile.flux  # -self.profile.flux[0] # do continuum subtraction
        velo_profile = self.profile.velo

        half_max = 0.5 * (np.max(flux_profile) + np.min(flux_profile))

        # search from the left side, but do not assume that the half max actually is on the left side.
        ileft = 0
        while flux_profile[ileft] <= half_max and ileft < len(flux_profile) - 1:
            ileft += 1
        # now from the right side
        iright = len(velo_profile) - 1
        while flux_profile[iright] <= half_max and iright > 0:
            iright -= 1

        return velo_profile[iright] - velo_profile[ileft]

    def convolve(self, R: float) -> float:
        """
        Convolves all the profiles (each inclination) for this line.
        simply calls :func:`DataLineProfile.convolve`

        Parameters
        ----------
        R :
            The desired spectral resolution.

        Returns
        -------
        float :
          The FWHM of the Gaussian in units of `km/s` i.e. the spectral resolution.
        """
        FWHM = None
        for i in range(len(self._inclinations)):
            FWHM = self._profiles[i].convolve(R)
        return FWHM

    def __str__(self):
        return f"Line: {self.ident:16} wl={self.wl:13.6f} μm  flux={self.flux:10.3e} W/m^2  inc={self.inclination:4.1f}°"


class ModelParameters(MutableMapping):
    """
    Access to the Parameters of a model. Reads Parameter.out and provides
    some utility functions fo access Parameters.

    """

    def __init__(self, filename="Parameter.out", directory="."):
        """
        Opens the file and fills a dictionary with all Parameters.
        The f90nml package is used, so type conversion is properly done.
        This dictionary is readonly.

        The get routine has some special treatment for certain parameters (e.g. return a list
        with the correct len). However, special treatment for some fields might be missing.

        Parameters
        ----------
        filename : string
          The Filename of the Parameter file. Default: Parameter.out

        directory : string
          The directory that contains the |prodimo| model output. Default: "."

        ..todo::
          - make some utility routine, mainly unit conversion, for fields like Mdisk etc.

        """
        fparams, fpath = _getfile(filename, directory=directory)
        self.mapping: nml.NameList = nml.read(fparams)["para"]

    def __getitem__(self, key):
        # some special treatments ... because we do not know the length of that array
        if key.upper() == "AGE_DISK":
            if self.mapping["time_dependent"] or self.mapping["time_chem_disk"]:
                nage = self.mapping["N_AGE"]
                return self.mapping[key][0:nage]
            else:
                return np.inf
        elif key.upper() == "INCL":
            if "nincl" in self.mapping.keys():
                nincl = self.mapping["nincl"]
                return self.mapping[key][0:nincl]
            else:
                return self.mapping[key]
        else:
            return self.mapping[key]

    def __delitem__(self, key):
        print("Don't delete Parameters ...")

    def __setitem__(self, key, value):
        print("Updating ModelParameters is not allowed ...")

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __str__(self):
        out = ""
        for key in self.mapping:
            out += key + " = " + str(self.mapping[key]) + "\n"
        return out


class DataFLiTsSpec(object):
    """
    Data container for a FLiTs spectrum.
    Currently provides only the wavelength grid and the flux in Jy, as produced
    by FLiTs.
    """

    def __init__(self):
        self.wl: np.ndarray[tuple[int], np.float64]
        """ Wavelength grid in micron. """
        self.flux: np.ndarray[tuple[int], np.float64]
        """ Flux in Jy. """
        self.flux_cont: np.ndarray[tuple[int], np.float64]
        """ Continuum flux of the spectrum in Jy. """
        self.conv_wl: np.ndarray[tuple[int], np.float64] | None = None
        """ Convolved Wavelength grid in micron. """
        self.conv_flux: np.ndarray[tuple[int], np.float64] | None = None
        """ Convolved Flux in Jy. """
        self.conv_flux_cont: np.ndarray[tuple[int], np.float64] | None = None
        """ Convolved Continuum flux of the spectrum in Jy. """
        self.conv_R: NDArray[np.float64] | None = None
        """ : Convolved spectrum. Unit: Jy."""

    def convolve(self, specR, sample=1, contReturn=False, inplace=False):
        """
        Returns a convolved version of the Spectrum.
        Does not change the original FLiTs spectrum.

        Parameters
        ----------
        specR : int
          The desired spectral resolution.

        Returns
        -------
        (tuple):
          tuple containing: wls(array_like): array of wavelength points in micron,
          flux(array_like): flux values for each wavelength point in Jansky.


        .. todo::

          allow for different units.
        """

        print("INFO: convolve FLiTs spectrum ... ")

        from astropy.convolution import convolve_fft
        from astropy.convolution import Gaussian1DKernel

        wl = self.wl
        flux = self.flux
        flux_cont = self.flux_cont

        # Make a new wl grid
        wl_log = np.logspace(
            np.log10(np.nanmin(wl)), np.log10(np.nanmax(wl)), num=np.size(wl) * sample
        )

        # Find stddev of Gaussian kernel for smoothing
        # taken from here https://github.com/spacetelescope/pysynphot/issues/78
        R_grid = (wl_log[1:-1] + wl_log[0:-2]) / (wl_log[1:-1] - wl_log[0:-2]) / 2
        sigma = np.median(R_grid) / specR
        if sigma < 1:
            sigma = 1

        # Interpolate on logarithmic grid
        f_log = np.interp(wl_log, wl, flux)
        f_cont_log = np.interp(wl_log, wl, flux_cont)

        # in the idl script this is interpreted as the FWHM,
        # but the convolution routine wants stddev use relation
        # FWHM=2*sqrt(2ln2)*stddev=2.355/stddev
        # this should than be consistent with the result from the
        # ProDiMo idl script
        gauss = Gaussian1DKernel(stddev=sigma / 2.355)
        flux_conv = convolve_fft(f_log, gauss)
        flux_cont_conv = convolve_fft(f_cont_log, gauss)

        # Interpolate back on original wavelength grid
        flux_sm = np.interp(wl, wl_log, flux_conv)
        flux_cont_sm = np.interp(wl, wl_log, flux_cont_conv)

        cut = 2 * int(sigma)
        flux_smc = flux_sm[cut : (len(flux_sm) - cut)]
        flux_cont_smc = flux_cont_sm[cut : (len(flux_cont_sm) - cut)]
        wlc = wl[cut : (len(wl) - cut)]

        self.conv_R = specR
        self.conv_wl = wlc
        self.conv_flux = flux_smc
        self.conv_flux_cont = flux_cont_smc

        if not inplace:
            if contReturn:
                return wlc, flux_smc, flux_cont_smc
            else:
                return wlc, flux_smc


class DataGas(object):
    """
    Holds the data for the gas (mainly from `dust_opac.out`).

    .. todo::

        - currently only the init cs is read, not the x,y data
    """

    def __init__(self, nlam):
        self.nlam = nlam
        self.lam = np.zeros(shape=(nlam))
        self.energy = np.zeros(
            shape=(nlam)
        )  # for convenience as often energy is also used for gas [eV]
        self.abs_cs = np.zeros(shape=(nlam))  # unit cm^2/H
        self.sca_cs = np.zeros(shape=(nlam))  # unit cm^2/H


class DataDust(object):
    """
    Holds the data for the dust (mainly from dust_opac.out)

    .. todo::

        - dust composition is not yet read.

    Attributes
    ----------

    """

    def __init__(self, amin, amax, apow, nsize, nlam):
        self.amin: float = amin
        """ : The minimum grain size of the size distribution. UNIT: micron """
        self.amax: float = amax
        """ : The maximum grain size of the size distribution. UNIT: micron """
        self.apow: float = apow
        """ : The powerlaw exponent of the grain size distribution. """
        self.nsize: int = nsize
        """ : The number for grain size bins """
        self.lam: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The wavelength grid for the dust opacities. UNIT: `micron` DIM: (nlam) """
        self.energy: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The energy grid for the dust opacities (for convenience). UNIT: eV DIM: (nlam) """
        self.kext: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The dust extinction coefficient for each wavelength per g of dust. UNIT: |cm^2g^-1| DIM: (nlam) """
        self.kabs: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The dust absorption coefficient for each wavelength per g of dust. UNIT: |cm^2g^-1| DIM: (nlam) """
        self.ksca: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The dust scattering coefficient for each wavelength per g of dust. UNIT: |cm^2g^-1| DIM: (nlam) """
        self.ksca_an: NDArray[np.float64] = np.zeros(shape=(nlam))
        """ : The dust anisotropic (approximation) scattering coefficient for each wavelength per g of dust. UNIT: |cm^2g^-1| DIM: (nlam) """
        self.asize: NDArray[np.float64] | None = None
        """ : The grain size for each size bin. UNIT: micron DIM: (nsize) """
        self.sigmaa: NDArray[np.float64] | None = None
        """ : The radial surface density profiles for each individual grain. size UNIT: |gcm^-2| DIM: (nsize,nr) """


class DataElements(object):
    """
    Data for the Element abundances (the input). Holds the data from `Elements.out`.
    The data is stored as `OrderedDict` (same order as in `Elements.out`) with the element names as keys.

    Attributes
    ----------
    """

    def __init__(self):
        self.abun: OrderedDict[str, float] = OrderedDict()
        """ : Ordered dictionary holding the element abundances relative to hydrogen. """
        self.abun12: OrderedDict[str, float] = OrderedDict()
        """ : abundances in the +12 notation """
        self.massRatio: OrderedDict[str, float] = OrderedDict()
        """ : mass ratios """
        self.amu: OrderedDict[str, float] = OrderedDict()
        """ : atomic mass unit """
        self.muHamu: float | None = None
        """ : `rho = muH*n<H>` with `muH/amu` from `Elements.out` """

    def __str__(self):
        output = "name   12    X/H\n"
        for key in self.abun12.keys():
            output = (
                output
                + "{:5s}".format(key)
                + " "
                + "{:6.3f}".format(self.abun12[key])
                + " "
                + "{:6.3e}".format(self.abun[key])
                + "\n"
            )
        return output


class DataSpecies(object):
    """
    Data for the Species (the input).

    Holds the data from `Species.out`.

    The data is stored as OrderedDict with the element names as keys.

    Attributes
    ----------
    """

    def __init__(self):
        self.mass: OrderedDict[str, float] = OrderedDict()
        """ : The mass of the species *UNIT:* g. """
        self.charge: OrderedDict[str, int] = OrderedDict()
        """ : The charge of the species *UNIT:* e. """
        self.chemPot: OrderedDict[str, float] = OrderedDict()
        """ : The chemical potential as determined by |prodimo|. """

    def get_spdata(self, name) -> tuple[float, int, float]:
        """
        Returns all data of the species with `name`.

        Parameters
        ----------

        name : str or int
          The name of the species.
          if int then use it as index

        Returns
        -------

        (mass,charge,chemPot)

        """
        if isinstance(name, int):
            return (
                list(self.mass.values())[name],
                list(self.charge.values())[name],
                list(self.chemPot.values())[name],
            )
        else:
            return (self.mass[name], self.charge[name], self.chemPot[name])

    def __str__(self):
        output = "Number of species: " + str(len(self.mass.keys())) + "\n"
        output += "{:16s} {:10s} {:5s} {:s}".format("Name", "mass [g]", "charge", "chemPot [eV]\n")
        for name, mass, charge, chemPot in zip(
            self.mass.keys(), self.mass.values(), self.charge.values(), self.chemPot.values()
        ):
            output += "{:<16s} {:7.2e} {:5d} {:12.4f}".format(name, mass, charge, chemPot) + "\n"
        return output


class DataBgSpec(object):
    """
    Background field input spectrum.

    .. todo::

      - is not yet included in Data_ProDiMo

    """

    def __init__(self, nlam):
        self.nlam = nlam
        self.lam = np.zeros(shape=(nlam))
        self.nu = np.zeros(shape=(nlam))
        self.Inu = np.zeros(shape=(nlam))


class Chemistry(object):
    """
    Data container for chemistry analysis.
    Holds the information for one particular molecule.

    Also provides some convenience functions for further analysis.

    """

    def __init__(self, name):
        """
        Parameters
        ----------
        name : string
          The name of the model (can be empty).

        Attributes
        ----------

        """
        self.name: str = name
        """ The name of the model (can be empty) """
        self.totfrate: NDArray
        """ Total formation rate at each spatial grid point. """
        self.totdrate: NDArray
        """ Total destruction rate at each spatial grid point. """
        self.gridf: NDArray
        """ Contains for each individual grid point a sorted list of the formation reactions including the index (0) and the rate (1) """
        self.gridd: NDArray
        """ Contains for each individual grid point a sorted list of the destruction reactions including the index (0) and the rate (1) """
        self.fridxs: list
        """ List of all formation reaction indices for this species. """
        self.dridxs: list
        """ List of all destruction reaction indices for this species. """
        self.species: str
        """ name of species for which the chamanalysis should be done """
        self.model: Data_ProDiMo
        """ A reference to the model, for which we do the analysis. """

    def reac_rates_ix_iz(
        self,
        ix: int = None,
        iz: int = None,
        locau: tuple[float, float] = None,
        lowRatesFrac: float = 1.0e-3,
    ):
        """
        Function that analyse the Chemistry manually via a point-by-point analysis for a given species.
        Shows the most important formation and destruction rates for the given point ix,iz (or in au via Parameter `locau`).

        Parameters
        ----------

        ix : x-index corresponding to desired radial location in grid, starting at 0

        iz : z-index corresponding to desired radial location in grid, starting at 0

        locau :
          the desired coordinates in au ``(x,z)``. The routine then finds the closest
          grid point for those coordinates.

        lowRatesFrac :
          Only rates with rate/total_rate > lowRatesFrac are printed. Default: 1.e-3
          This is useful to avoid printing all the reactions that are not important.
        """

        model = self.model
        if locau is not None:
            ix = np.argmin(np.abs(model.x[:, 0] - locau[0]))
            iz = np.argmin(np.abs(model.z[ix, :] - locau[1]))

        if ix is None or iz is None:
            print("Please provide either ix,iz or locau!")
            return

        print("Analysing point x=", str(model.x[ix, iz]) + " au z=" + str(model.z[ix, iz]) + " au")

        print("      Detailed reaction rates for: %10s" % self.species)
        print(
            "------------------------------------------------------------------------------------------------------"
        )

        print("                    grid point = %i       %i" % (ix, iz))
        print("        r,z [au] (cylindrical) = %.3f  %.4f" % (model.x[ix, iz], model.z[ix, iz]))
        print(
            "               n<H>,nd [cm^-3] = %.1e  %.1e" % (model.nHtot[ix, iz], model.nd[ix, iz])
        )
        print("                Tgas,Tdust [K] = %.1e  %.1e" % (model.tg[ix, iz], model.td[ix, iz]))
        print(
            "                 AV_rad,AV_ver = %.1e  %.1e"
            % (model.AVrad[ix, iz], model.AVver[ix, iz])
        )
        print(
            "          %10s" % self.species
            + " abundance = %e" % model.getAbun(self.species)[ix, iz]
        )
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print(" Total form. rate [cm^-3 s^-1] = {:10.2e}".format(self.totfrate[ix, iz]))
        for i, ridx in enumerate(self.gridf[ix, iz, 0]):
            rate = self.gridf[ix, iz, 1][i]
            if rate / self.totfrate[ix, iz] > lowRatesFrac:  # don't print low rates
                print(
                    self.reac_to_str(
                        model.chemnet.reactions[ridx - 1],
                        list(self.fridxs).index(ridx) + 1,
                        rate=rate,
                    )
                )
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print(" Total dest. rate [cm^-3 s^-1] = {:10.2e}".format(self.totdrate[ix, iz]))
        for i, ridx in enumerate(self.gridd[ix, iz, 0]):
            rate = self.gridd[ix, iz, 1][i]
            if rate / self.totdrate[ix, iz] > lowRatesFrac:  # don't print unimportant rates
                print(
                    self.reac_to_str(
                        model.chemnet.reactions[ridx - 1],
                        list(self.dridxs).index(ridx) + 1,
                        rate=rate,
                    )
                )
        print(
            "------------------------------------------------------------------------------------------------------"
        )
        print("")

    def reac_to_str(self, reac, idx, rate=None):
        """
        Converts a Reaction to the output format we want for the chemanalysis.

        Parameters
        ----------
        reac : :class:`prodimopy.chemistry.network.Reaction`

        """
        # build the prods string assuming max three products
        reacstr = "".join(["{:13s}".format(p) for p in reac.reactants])
        reacstr += "".join(["{:13s}".format("") for p in range(3 - len(reac.reactants))])
        prodstr = "".join(["{:13s}".format(p) for p in reac.products])
        prodstr += "".join(["{:13s}".format("") for p in range(4 - len(reac.products))])
        if rate is not None:
            ratestr = "{:9.2e}".format(rate)
        else:
            ratestr = ""
        return "{:5d} {:6d} {:2s} {:<s} -> {:<s} {:<s}".format(
            idx, reac.id, reac.type, reacstr, prodstr, ratestr
        )

    def get_reac_grid(self, level, rtype):
        """
        Gets the counting index of the `x`  important Reaction. If it does not exist
        it is set to 0.

        Parameters
        ----------

        level : int
          The level of importance `1` means most important, `2` second most important etc.

        type : str
          Formation (pass `f`) or destruction Reaction (pass `d`)


        Returns
        -------
        tuple :
          And array of shape (model.nx,model.nz) where the first one contains the index
          of the Reactions for the list of reactions from chemanalysis (the output file)
          and the second one the rate itself (for this Reaction at each point).

        """
        if rtype == "d":
            grid = self.gridd
            ridxs = self.dridxs
        else:
            grid = self.gridf
            ridxs = self.fridxs

        nx = grid.shape[0]
        nz = grid.shape[1]

        gidx = np.zeros(shape=(nx, nz), dtype=int)
        grate = np.zeros(shape=(nx, nz))
        for ix in range(nx):
            for iz in range(nz):
                idxs = grid[ix, iz, 0]

                if len(idxs) < level:
                    val = 0
                    rate = 0.0
                else:
                    val = list(ridxs).index(idxs[level - 1]) + 1
                    rate = grid[ix, iz, 1][level - 1]

                gidx[ix, iz] = val
                grate[ix, iz] = rate

        return gidx, grate


class DataLineObs(DataLine):
    """
    Holds the observational data for one line.

    Differently to DataLine DataLineObs does not care about
    multiple inclinations. So simply some setter and getters are used
    to fill the list quantities (first entry).

    Attributes
    ----------
    """

    def __init__(self, flux, flux_err, fwhm, fwhm_err, flag):
        super(DataLineObs, self).__init__()
        self.flux = flux
        self.flux_err = flux_err
        self.fwhm = fwhm
        self.fwhm_err = fwhm_err
        self.flag = flag.lower()
        self.profile = None
        self.profileErr = None

    @property
    def flux(self):
        return self._fluxs[0]

    @flux.setter
    def flux(self, flux):
        self._fluxs.append(flux)

    @property
    def profile(self):
        # FIXME: Check what happens if _profiles is empty
        return self._profiles[0]

    @profile.setter
    def profile(self, value):
        # Not very nice, but per definition there can be only one line profile
        # from the observations (this avoids multiple entries)
        if len(self._profiles) > 0:
            self._profiles[0] = value
        else:
            self._profiles.append(value)


class Data_ProDiMo(object):
    """
    Data container for most of the output produced by |prodimo|.

    The class also includes some convenience functions and derives/calculates
    some additional quantities not directly included in the |prodimo| output.


    .. todo::

        - maybe put all the (real) observational data into one object (e.g. also the lines) e.g.DataObservations
        - maybe also have something like DataObservables (hold, SED, imaged, lines etc.)

    """

    def __init__(self, name: str):
        """

        Parameters
        ----------
        name : string
          The name of the model (can be empty).

        Attributes
        ----------

        """

        self.name: str = name
        """ : The name of the model (can be empty). """
        self.directory: str | None = None
        """ : The directory from which the model was read. Is e.g. set by :func:`~prodimopy.read.read_prodimo`. Can be a relative path. """
        self.__fpFlineEstimates = None  # The path to the FlineEstimates.out File
        self.__versionFlineEstimates = None  # the version of the formation of FlineEstimates.out
        self.params: ModelParameters
        """ : Dictionary that allows to access the models Parameters from Parameter.out. """
        self.nx: int
        """ : The number of spatial grid points in the x (radial) direction """
        self.nz: int
        """ : The number of spatial grid points in the z (vertical) direction """
        self.nspec: int | None = None  # allow None, mainly for test purposes
        """ : The number of chemical species included in the model. """
        self.nheat: int
        """ : The number of heating processes included in the model. """
        self.ncool: int
        """ : The number of cooling processes included in the model. """
        self.p_dust_to_gas: float
        """ : The global dust to gas mass ratio (single value, given Parameter). """
        self.p_v_turb: float
        """ : The global turbulent velocity (single value). *UNIT:* |kms^-1| """
        self.p_rho_grain: float
        """ : The global grain mass density (the density of one dust grain). *UNIT:* |gcm^-3|. """
        self.p_mdisk: float
        """ : The disk mass in solar units. Is taken from ProDiMo.out. Represents the parameter value.
            Please note if also an envelope is included or the structure comes from a 1D or 2D interface this value is not the actually disk mass.
        """
        self.td_fileIdx: int | None = None
        """ : The file index (prefix) in case of a time-dependent chemistry model (Starts at 1). """
        self.age: float = np.inf
        """ : The age of the model in years. Is taken from ``Parameter.out``. ``np.inf`` for steady-state model. *UNIT:* years. """
        self.x: NDArray[np.float64]
        """ : The x coordinates (radial direction). *UNIT:* au, *DIMS:* (nx,nz) """
        self.z: NDArray[np.float64]
        """ : The z coordinates (vertical direction). *UNIT:* au, *DIMS:* (nx,nz) """
        self.rhog: TGridfloat
        """ : The gas density. *UNIT:* |gcm^-3|, *DIMS:* (nx,nz) """
        self.rhod: TGridfloat
        """ : The dust density. *UNIT:* |gcm^-3|, *DIMS:* (nx,nz) """
        self.d2g: TGridfloat
        """ : The dust to gas mass ratio from |prodimo| *UNIT:* , *DIMS:* (nx,nz)"""
        self.nHtot: TGridfloat
        """ : The total hydrogen number density. *UNIT:* |cm^-3|, *DIMS:* (nx,nz) """
        self.muH: float
        """ : The conversion constant from `nHtot` to `rhog`. It is assumed that it is constant throughout the disk. 
            It is given by ``rhog/nHtot``. *UNIT:* g. 
        """
        self.NHver: TGridfloat
        """ : Vertical total hydrogen column density. ``nHtot`` is integrated from the disk surface to the midplane at each radial grid point. 
            The intermediate results are stored at each grid point. For example ``NHver[:,0]`` gives the total column density as a function of radius.
            *UNIT:* |cm^-2|, *DIMS:* (nx,nz).
        """
        self.NHrad: TGridfloat
        """ : Radial total hydrogen column density. Integrated along radial rays, starting from the star. 
            Otherwise same behaviour as :attr:`~prodimopy.read.Data_ProDiMo.NHver`. *UNIT:* |cm^-2|, *DIMS:* (nx,nz)
        """
        self.nd: TGridfloat
        """ : The dust number density. *UNIT:* |cm^-3|, *DIMS:* (nx,nz). """
        self.tg: TGridfloat
        """ : The gas temperature. *UNIT:* K, *DIMS:* (nx,nz). """
        self.td: TGridfloat
        """ : The dust temperature. *UNIT:* K, *DIMS:* (nx,nz). """
        self.pressure: TGridfloat
        """ : The gas pressure. *UNIT:* |ergcm^-3|, *DIMS:* (nx,nz). """
        self.soundspeed: TGridfloat
        """ : The isothermal sound speed. *UNIT:* |kms^-1|, *DIMS:* (nx,nz). """
        self.velocity: TGridfloat
        """ : The velocity field (vector) given as vx,vy,vz. *UNIT:* |kms^-1|, *DIMS:* (nx,nz,3). """
        self.damean: TGridfloat
        """ : The mean dust particle radius. Is defined as `<a3>**(1/3)`. *UNIT:* micron, *DIMS:* (nx,nz)."""
        self.da2mean: TGridfloat
        """ : The surface weighted mean dust particle radius. *UNIT:* micron, *DIMS:* (nx,nz) """
        self.dNlayers: TGridfloat
        """ : The number of ice layers on the dust grains. *DIMS:* (nx,nz). """
        self.Hx: TGridfloat
        """ : The X-ray energy deposition rate per hydrogen nuclei. *UNIT:* erg <H>\\ :sup:`-1`, *DIMS:* (nx,nz). """
        self.zetaX: TGridfloat
        """ : X-ray ionisation rate per hydrogen nuclei. *UNIT:* |s^-1|, *DIMS:* (nx,nz). """
        self.zetaCR: TGridfloat
        """ : Cosmic-ray ionisation rate per molecular hydrogen (H2) *UNIT:* |s^-1|, *DIMS:* (nx,nz). """
        self.zetaSTCR: TGridfloat
        """ : Stellar energetic particle ionisation rate per H2. *UNIT:* |s^-1|, *DIMS:* (nx,nz). """
        self.tauX1: TGridfloat
        """ : Radial optical depth at 1 keV (for X-rays). *DIMS:* (nx,nz). """
        self.tauX5: TGridfloat
        """  : Radial optical depth at 5 keV (for X-rays). *DIMS:* (nx,nz). """
        self.tauX10: TGridfloat
        """ : Radial optical depth at 10 keV (for X-rays). *DIMS:* (nx,nz). """
        self.AVrad: TGridfloat
        """ : Radial visual extinction (measured from the star outwards). *DIMS:* (nx,nz). """
        self.AVver: TGridfloat
        """ : Vertical visual extinction (measured from the disk surface to the mid-plane). *UNIT:*, *DIMS:* (nx,nz). """
        self.AV: TGridfloat
        """ : Given by ``min([AVver[ix,iz],AVrad[ix,iz],AVrad[nx-1,iz]-AVrad[ix,iz]])``, hence the lowest visual extinction at a certain point. 
              It is assumed radiation can escape either vertically upwards, radially inwards or radially outwards. *DIMS:* (nx,nz).
        """
        self.nlam: int
        """ : The number of wavelength bands used in the continuum radiative transfer. """
        self.lams: NDArray[np.float64]
        """ : The band wavelengths (centers) considered in the radiative transfer. *UNIT:* microns, *DIMS:* (nlam). """
        self.lambs: NDArray[np.float64] | None = None
        """ : The band wavelengths (edges) considered in the radiative transfer. *UNIT:* microns, *DIMS:* (nlam+1). 
              This can be `None` as the edges wavelengths are only available with XrayRT or gasRT mode. 
        """
        self.chi: NDArray[np.float64]
        """ : Geometrical UV radiation field in units of the Drain field. *UNIT:* Draine field, *DIMS:* (nx,nz). """
        self.chiRT: NDArray[np.float64]
        """ : UV radiation field as properly calculated in the radiative transfer, in units of the Drain field. *UNIT:* Draine field, *DIMS:* (nx,nz). """
        self.kappaRos: TGridfloat | None = None
        """ : Rosseland mean opacity. In case of gas radiative transfer for the dust plus the gas. *UNIT:* |cm^-1|, *DIMS:* (nx,nz). """
        self.tauchem: TGridfloat
        """ : Chemical timescale (steady-state) *UNIT:* yr, *DIMS:* (nx,nz). """
        self.taucool: TGridfloat
        """ : Cooling timescale. *UNIT:* yr, *DIMS:* (nx,nz). """
        self.taudiff: TGridfloat
        """ : Vertical radiative diffusion timescale (using the Rosseland mean opacities). *UNIT:* yr, *DIMS:* (nx,nz). """
        self.spnames: typing.Dict[str, int]
        """ : Dictionary providing the index of a particular species (e.g. spnames["CO"]). This index can be used for arrays having an species dimension (like nmol). 
            The electron is included. *DIMS:* (nspec). """
        self.solved_chem: NDArray[np.int32]  # FIXME: I think the doc is not up-to-date any more
        """ : Flag for chemistry solver (values, 0,1,2) (see |prodimo| code). 1 means everything okay, 0 failure, 2 time-dependent step needed. *DIMS:* (nx,nz). """
        self.rateH2form: TGridfloat
        """ : The H2 formation ratio. *UNIT:* |s^-1|, *DIMS:* (nx,nz). """
        self.rateH2diss: np.ndarray[tuple[int, int, int], np.float64]
        """ : The different H2 dissociation rates. *UNIT:* |s^-1|, *DIMS:* (nx,nz,3). """
        self.isoratio_12CO13CO: TGridfloat | None = None
        """ : Isotope ratio of 12CO to 13CO, if it was estimated in the model. *DIMS:* (nx,nz) """
        self.heat_names: list[str]
        """ All the names of the heating processes. """
        self.cool_names: list[str]
        """ All the names of the cooling processes. """
        self.heat_mainidx: NDArray[np.int32]
        """ : Index of the main heating process at the given grid point. *UNIT:* , *DIMS:* (nx,nz). """
        self.cool_mainidx: NDArray[np.int32]
        """ : Index of the main cooling process at the given grid point. *UNIT:* , *DIMS:* (nx,nz). """
        self.lineEstimates: list[DataLineEstimate] | None = None
        """ : All the line estimates from FlineEstimates.out. Each spectral line in FlineEstimates corresponds to one :class:`prodimopy.read.DataLineEstimate` object. """
        self.lines: list[DataLine] | None = None
        """ : All the spectral lines from `line_flux.out` (proper Line transfer). Each spectral line in `line_flux.out` is represented by one :class:`prodimopy.read.DataLine` object.
            This also includes multiple inclinations.
        """
        self._sed: DataSED | None = None
        """ : The Spectral Energy Distribution for the model (SED) as calculated in the radiative transfer with ray tracing. Can only be accessed via getter setter
            to deal with inclinations. See :class:`prodimopy.read.DataSED` for details.
        """
        self.contImages: DataContinuumImages | None = None
        """ : Holds the continuum images data (image.out) if available. The full images are only read if requested for a particular wavelength. """
        self.star: DataStar | None = None
        """ : The stellar properies including the (unattenuated) input spectrum. """
        self.gas: DataGas | None = None
        """ : Holds various properties of the gas component (e.g. opacities). """
        self.dust: DataDust | None = None
        """ : Holds various properties of the dust component (e.g. opacities). """
        self.env_dust: DataDust | None = None
        """ : Holds various properties of the dust component (e.g. opacities) of the envelope. Only relevant if |prodimo| is used in the envelope mode. """
        self.elements: DataElements
        """ : Holds the element abundances (Elements.in) """
        self.species: DataSpecies
        """ : Holds the initial species data (Species.in). """
        self.sedObs: DataContinuumObs | None = None
        """ : Holds the provided SED observations (photometry, spectra, extinction etc.)."""
        self.lineObs: list[DataLineObs] | None = None
        """ : Holds the provide line observations (e.g. LINEObs.dat and line profiles). """
        self.FLiTsSpec: DataFLiTsSpec | None = None
        """ : Holds the FLiTs spectrum if it exists. """
        self._log: bool = True
        """ : Allows to switch off some log statements (not consistently implemented yet). """
        self._pAUtocm: float = 1.495978700e13
        """ : Conversion factor from AU to cm taken directly from |prodimo|. """
        #
        # these are some cache variables for lazy initialization. Using them allows to do
        # conversions/calculations only if the quantities are accessed (used)
        #
        self._cool_cache: NDArray = None
        self._cool: NDArray = None
        self._heat_cache: NDArray = None
        self._heat: NDArray = None
        self._radFields_cache: NDArray = None
        self._radFields: NDArray = None
        self._nmol_cache: NDArray = None
        self._nmol: NDArray = None
        self._sdg: NDArray = None
        self._sdd: NDArray = None
        self._vol: NDArray = None
        self._cdnmol: NDArray = None
        self._rcdnmol: NDArray = None
        self._chemnet: pcnet.ReactionNetworkPout = None

    @property
    @deprecated("Use model.star.mass instead.")
    def mstar(self) -> float:
        """: The stellar mass in solar units. Is taken from ProDiMo.out
        Deprecated: use :attr:`~prodimopy.read.DataStar.mass` instead.
        """
        return self.star.mass

    @property
    @deprecated("Use model.star instead.")
    def starSpec(self) -> DataStar:
        """: The stellar properties including the (unattenuated) input spectrum.
        Deprecated: use :attr:`~prodimopy.read.Data_ProDiMo.star` instead.
        """
        return self.star

    @property
    def sed(self) -> DataSED | None:
        """: Not sure if this is the best solution, but need a getter. It returns the SED for the current inclination."""
        return self._sed

    @sed.setter
    def sed(self, value: DataSED):
        """Set the SED for the current inclination"""
        self._sed = value

    @property
    def nmol(self) -> NDArray[np.float64]:
        """: Number densities of all chemical species (mainly molecules). *UNIT:* |cm^-3|, *DIMS:* (nx,nz,nspec)."""
        if self._nmol_cache is not None:
            self._nmol = np.array(self._nmol_cache, dtype=np.float64)
            self._nmol_cache = None  # remove the string cache
        return self._nmol

    @nmol.setter
    def nmol(self, value):
        self._nmol = value

    @property
    def cdnmol(self) -> NDArray[np.float64]:
        """: Vertical column number densities for each chemical species at each point in the disk. Integrated from the surface to the midplane at each radial grid point.
        *UNIT:* |cm^-2|, *DIMS:* (nx,nz,nspec).
        """
        if self._cdnmol is None:
            _calc_cdnmol(self)
        return self._cdnmol

    @cdnmol.setter
    def cdnmol(self, value):
        self._cdnmol = value

    @property
    def rcdnmol(self) -> NDArray[np.float64]:
        """: Radial column number densities for each species at each point in the disk. Integrated from the star outwards along fixed radial rays given by the vertical grid.
        *UNIT:* |cm^-2|, *DIMS:* (nx,nz,nspec)
        """
        if self._rcdnmol is None:
            _calc_rcdnmol(self)
        return self._rcdnmol

    @rcdnmol.setter
    def rcdnmol(self, value):
        self._rcdnmol = value

    @property
    def sdg(self) -> NDArray[np.float64]:
        """: The gas vertical surface density. This is for only one half of the disk (i.e. from z=0 to z+), like in |prodimo|. For the total surface density multiply by two.
        *UNIT:* |gcm^-2|, *DIMS:* (nx,nz)
        """
        if self._sdg is None:
            calc_surfd(self)
        return self._sdg

    @sdg.setter
    def sdg(self, value: NDArray):
        self._sdg = value

    @property
    def sdd(self) -> NDArray[np.float64]:
        """: The dust vertical surface density. This is for only one half of the disk (i.e. from z=0 to z+), like in |prodimo|. For the total surface density multiply by two.
        *UNIT:* |gcm^-2|, *DIMS:* (nx,nz)
        """
        if self._sdd is None:
            calc_surfd(self)
        return self._sdd

    @sdd.setter
    def sdd(self, value):
        self._sdd = value

    @property
    def cool(self) -> NDArray[np.float64]:
        """: Cooling rates for the various cooling processes. *UNIT:* |ergcm^-3s^-1| *DIMS:* (nx,nz,ncool)."""
        if self._cool_cache is not None:
            self._cool = np.array(self._cool_cache, dtype=float)
            self._cool_cache = None  # remove the string cache
        return self._cool

    @cool.setter
    def cool(self, value):
        self._cool = value

    @property
    def heat(self) -> NDArray[np.float64]:
        """: Heating rates for the various heating processes. *UNIT:* |ergcm^-3s^-1| *DIMS:* (nx,nz,nheat)."""
        if self._heat_cache is not None:
            self._heat = np.array(self._heat_cache, dtype=np.float64)
            self._heat_cache = None  # remove the string cache
        return self._heat

    @heat.setter
    def heat(self, value):
        self._heat = value

    @property
    def radFields(self) -> NDArray[np.float64]:
        """ : Radiation field (mean intensity) for each wavelength band. *UNIT:* erg |s^-1| |cm^-2| |sr^-1| |Hz^-1|, *DIMS:* (nx,nz,nlam)."""
        if self._radFields_cache is not None:
            self._radFields = np.array(self._radFields_cache, dtype=np.float64)
            self._radFields_cache = None  # remove the string cache now
        return self._radFields

    @radFields.setter
    def radFields(self, value):
        self._radFields = value

    @property
    def vol(self) -> NDArray[np.float64]:
        """: The volume for each grid point. *UNIT:* |cm^3|, *DIMS:* (nx,nz)."""
        if self._vol is None:
            _calc_vol(self)
        return self._vol

    @vol.setter
    def vol(self, value):
        self._vol = value

    @property
    def chemnet(self) -> pcnet.ReactionNetworkPout:
        """The chemical reactions of the model. Holds what is in ``Reactions.out``. Is only read if needed."""
        if self._chemnet is None:
            self._chemnet = pcnet.ReactionNetworkPout(name=self.name, modeldir=self.directory)
        return self._chemnet

    @chemnet.setter
    def chemnet(self, value: pcnet.ReactionNetworkPout):
        self._chemnet = value

    @property
    def velocity_xz(self) -> NDArray[np.float64]:
        """:
        The absolute xz-component of the :attr:`velocity` field. *UNIT:* |kms^-1|, *DIMS:* (nx,nz).
        """

        return np.sqrt((self.velocity[:, :, 0]) ** 2 + (self.velocity[:, :, 2]) ** 2)

    def __str__(self):
        output = "Info ProDiMo.out: \n"
        output += "NX: " + str(self.nx) + " NZ: " + str(self.nz) + " NSPEC: " + str(self.nspec)
        output += (
            " NLAM: "
            + str(self.nlam)
            + " NCOOL: "
            + str(self.ncool)
            + " NHEAT: "
            + str(self.nheat)
        )
        output += "\n"
        output += "p_dust_to_gas: " + str(self.p_dust_to_gas)
        return output

    def _getLineIdx(self, wl, ident=None):
        if self.lines is None:
            return None

        wls = np.array([line.wl for line in self.lines])

        if ident is not None:
            linestmp = [line for line in self.lines if line.ident == ident]
            if linestmp is not None and len(linestmp) > 0:
                wlstmp = np.array([line.wl for line in linestmp])
                itmp = np.argmin(abs(wlstmp[:] - wl))
                # get the index of the whole line array, trusting python.
                idx = self.lines.index(linestmp[itmp])
                # super security check, should not happen so throw and exception
                if self.lines[idx].ident != ident:
                    raise ValueError(
                        "Something is wrong found: ident",
                        self.lines[idx].ident,
                        " and wl ",
                        self.lines[idx].wl,
                        " for ",
                        ident,
                        wl,
                    )
                else:
                    return idx
            else:
                print("WARN: No line found with ident", ident, " and wl ", wl)
                return None
        else:
            idx = np.argmin(abs(wls[:] - wl))

            if (abs(wls[idx] - wl) / wl) > 0.01:
                print("WARN: No line found within 1% of the given wavelength:", wl)
                return None
            else:
                return idx

    def sedinc(self, incidx: int = 0) -> DataSED:
        """
        Get the SED for for the given inclination index ``iinc``.

        Parameters
        ----------
        incidx :
          The inclination index for which the SED should be retrieved.

        Returns
        -------
        DataSED
          The SED for the specified inclination index.

        """
        assert self._sed is not None
        nincs = len(self._sed._inclinations)
        if nincs == 1:
            self._sed._incidx = 0
        elif incidx >= nincs:
            self._sed._incidx = nincs - 1
        else:
            self._sed._incidx = incidx
        return self._sed

    def getSEDAnaMask(self, lam):
        """
        Returns a numpy mask where only the grid points outside the emission
        origin area for the given wavelength (continuum) are marked as invalid.

        This mask can be used in e.g. :func:`~prodimopy.read.Data_ProDiMo.avg_quantity`

        .. warning::

            in case of optically thin emission only the points of one half
            of the disk are considered. In that case an average quantity of this
            box(mask) will not be completely correct.

        Parameters
        ----------
        lam : float
          the wavelength for which the emission origin region should be determined:
          UNITS: micron

        Returns
        -------
        array_like(float,ndim=2)
          Numpy mask with *DIMS:* (nx,nz)

        """
        assert self.sed is not None

        sedAna = self.sed.sedAna
        x15 = interp1d(sedAna.lams, sedAna.r15, bounds_error=False, fill_value=0.0, kind="linear")(
            lam
        )
        x85 = interp1d(sedAna.lams, sedAna.r85, bounds_error=False, fill_value=0.0, kind="linear")(
            lam
        )

        mask = np.ones(shape=(self.nx, self.nz))
        for ix in range(self.nx):
            if self.x[ix, 0] >= x15 and self.x[ix, 0] <= x85:
                z85 = interp1d(
                    sedAna.lams,
                    sedAna.z85[:, ix],
                    bounds_error=False,
                    fill_value=0.0,
                    kind="linear",
                )(lam)
                z15 = interp1d(
                    sedAna.lams,
                    sedAna.z15[:, ix],
                    bounds_error=False,
                    fill_value=0.0,
                    kind="linear",
                )(lam)
                for iz in range(self.nz):
                    if self.z[ix, iz] <= z15 and self.z[ix, iz] >= z85:
                        mask[ix, iz] = 0

        return mask

    def getLine(self, wl: float, ident: str = None, incidx: int = 0) -> DataLine | None:
        """
        Returns the spectral line (from the line RT) closest to the given wavelength.

        Parameters
        ----------
        wl :
          The wavelength which is used for the search. *UNIT:* micron.

        ident :
          A line identification string which should also be considered for the search.

          Please note that it is not the chemical species name. For example if you have to lines
          for the same CO transition but one for NLTE (``ident=CO``) and one for LTE (``ident=CO_lte``)
          the species will be the same in both. To properly select those lines you need to
          provided the ident as the wl is identical.

        incidx :
          select the inclination for the line. (default: 0) . 0 means
          the first one. If only one inclination exists always this one will be used
          (i.e. the value of incidx is ignored).

        Returns
        -------
        DataLine
          Returns `None` if no lines are included in the model.

        """

        idx = self._getLineIdx(wl, ident=ident)

        if idx is None:
            return None
        else:
            assert self.lines is not None
            line = self.lines[idx]
            if len(line._inclinations) == 1:
                line._incidx = 0
            else:
                # only here I want to really set it
                line._incidx = incidx
            return line

    def selectLines(self, ident: str) -> list[DataLine] | None:
        """
        Returns a list of all line fluxes included in the line transfer, for the given line ident.

        Parameters
        ----------
        ident :
          The line identification (species name) as defined in |prodimo|.
          The ident is not necessarily equal to the underlying chemical species
          name (e.g. isotopologues, ortho-para, or cases like N2H+ and HN2+)

        Returns
        -------
        list[DataLine] :
          All lines for the given ident, or an empty list if nothing was found.
          ``None`` if no lines are available at all.

        """
        if self.lines is None:
            return None

        lines = list()
        for le in self.lines:
            if le.ident == ident:
                lines.append(le)

        return lines

    def gen_specFromLineEstimates(
        self,
        wlrange=[10, 15],
        ident: str | None = None,
        specR=3000,
        unit="W",
        contOnly=False,
        noCont=False,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """
        Generates a "Spectrum" from the line estimates results of |prodimo| and
        convolves it to the given spectral resolution.
        If the SED was also calculated the line fluxes will be added to the continuum,
        if not a continuum of zero flux is assumed.

        This routine can become very slow, depending on the number of lines
        within a given wavelength range. It can be more efficient to produce smaller
        chunks with not so many lines.

        Parameters
        ----------
        wlrange : array_like
          Generate the spectrum in the wavelength range [start,end]
          Default: `[10,15]` Units: micron

        ident : str
          only the lines with this ident (like given in the line estimates) are
          considered. Default: `None` (all lines in the given wlrange are considered)

        specR : int
          the desired spectral resolution. If `None` a spectrum with simple the
          line fluxes added (i.e. as "delta function") is returned.
          Default: `3000`

        unit : str
          desired unit for the output. Current choices `W` (W/m^2/Hz) or 'Jy' (Jansky).
          `W` is the default option.

        contOnly : boolean
          only do it for the continuum (do not add any lines).
          Default: `False`

        noCont : boolean
          assume zero continuum
          Default: `False`

        Returns
        -------
        (tuple):
          tuple containing: wls(array_like): array of wavelength points in micron,
          flux(array_like): flux values for each wavelength point in |Wm^-2Hz^-1|
          or Jy (depending on the `unit` parameter)

        """
        import astropy.convolution as conv

        # one can call the routine like this ([5,10],3000). However, 3000 will be taken as the ident
        # try to catch this case
        if ident is not None and isinstance(ident, (int, float)):
            specR = ident
            ident = None

        startT = timer()

        lmin = wlrange[0] / 1.0e4
        lmax = wlrange[1] / 1.0e4
        R = 1.0e6
        if specR is not None and specR > (0.1 * R):
            print(
                "WARN: requested spectral resolution is too high use " + str(0.1 * R) + " instead"
            )

        # technical spectral resolution

        # determine the number of points required
        del_loglam = np.log10(1.0 + 1.0 / R)  # log(lam+dlam)-log(lam)
        N = 1 + int(np.log10(lmax / lmin) / del_loglam)

        mwlsline = np.logspace(np.log10(lmin), np.log10(lmax), N)

        if self.sed is None or noCont:
            contfluxline = mwlsline * 0.0  # no continuum
        else:
            contfluxline = np.interp(mwlsline, self.sed.lam / 1.0e4, self.sed.fnuErg)

        # do everything in cgs units
        confac = (1.0 * (u.W / (u.m**2))).to(u.erg / u.s / (u.cm**2)).value
        lineest = self.selectLineEstimates(ident=ident, wlrange=wlrange)
        # print("INFO: gen_specFromLineEstimates: build spectrum for "+
        #      str(len(lineest))+" lines ...")
        # this loop is taking most of the time , not the convolution.
        # I guess that could still be faster, but that might require a lot more
        # memory
        #     from tqdm import tqdm
        #     for line in tqdm(lineest):
        tonu = const.c.cgs.value / R
        for line in tqdm(lineest, "INFO: gen_specFromLineEstimates: build spectrum: "):
            wlcm = line.wl / 1.0e4
            # Find the closes wavelength point in the new grid.

            # idx=np.argmin(np.abs(mwlsline-wlcm))
            # this does the same as above but seems to be 10 times faster
            idx = np.argmax(mwlsline > (wlcm))
            if (mwlsline[idx] - wlcm) > (wlcm - mwlsline[idx - 1]):
                idx -= 1

            # like in the idl script
            # R=mwlsline[idx]/(mwlsline[idx]-mwlsline[idx-1])
            # print(R)
            # just use delta functions -> line profile is a delta function
            if not contOnly:
                if specR is None:
                    contfluxline[idx] = contfluxline[idx] + (line.flux * confac)
                else:
                    dnu = tonu / wlcm
                    contfluxline[idx] = contfluxline[idx] + (line.flux * confac) / dnu

        print("INFO: gen_specFromLineEstimates: convolve spectrum ...")

        if specR is None:
            FWHMpix = 1.0
            mwlslinez = mwlsline
            contfluxline_conv = contfluxline
        else:
            # in the idl script this is interpreted as the FWHM,
            # but the convolution routine wants stddev use relation
            # FWHM=2*sqrt(2ln2)*stddev=2.355/stddev
            # this should than be consistent with the result from the
            # ProDiMo idl script
            FWHMpix = R / specR
            g = conv.Gaussian1DKernel(stddev=FWHMpix / 2.355, factor=7)

            # Convolve data
            contfluxline_conv = conv.convolve(contfluxline, g)
            # print(z)
            # remove beginning and end ... strange values
            cut = 2 * int(FWHMpix)
            contfluxline_conv = contfluxline_conv[cut : (len(contfluxline_conv) - cut)]
            mwlslinez = mwlsline[cut : (len(mwlsline) - cut)]

        # now downgrade the grid to something reasonable
        outwls = np.linspace(
            np.min(mwlslinez), np.max(mwlslinez), int(len(mwlsline) / FWHMpix) * 5
        )
        outflux = np.interp(outwls, mwlslinez, contfluxline_conv)

        outflux = outflux / confac
        if unit == "Jy":
            outflux = (outflux * u.W / u.m**2 / u.Hz).to(u.Jy).value

        print("INFO: time: ", "{:4.2f}".format(timer() - startT) + " s")

        return outwls * 1.0e4, outflux

    def getLineEstimate(self, ident, wl):
        """
        Finds and returns the line estimate for the given ident which is closest
        to the given wavelength. If the ident is unknown None is returned. If the ident
        exist the routine always returns an line estimate object.

        Parameters
        ----------
        ident : string
          The line identification string. Note that the ident is not necessarily equal to the
          corresponding chemical species.

        wl : float
          the wavelength which is used for the search. *UNIT:* micron.

        Returns
        -------
        :class:`prodimopy.read.DataLineEstimate`
          Returns `None` if the line estimate is not found.

        Notes
        -----
          The parameters of this method are not consistent
          with :meth:`~prodimopy.read.Data_ProDiMo.getLine`. This might be confusing.
          However, there is a reason for this. The number of
          included line estimates in a |prodimo| model can be huge and just searching
          with the wavelength might become slow. However, this probably can be improved.

          To speed up the reading of `FlineEstimate.out` the extra radial info
          (see :class:`~prodimopy.read.DataLineEstimateRInfo` of all the line estimates
          is not read. However, in this routine it is read for the single line estimate
          found. One should use this routine to access the radial info for a single line estimate.
        """
        found = -1
        i = 0
        mindiff = 1.0e20

        if self.lineEstimates is None:
            print("WARN: No lineEstimates are included (or not read) for this model.")
            return None

        # print ident, wl
        for le in self.lineEstimates:
            if le.ident == ident:
                diff = abs(le.wl - wl)
                if diff < mindiff:
                    found = i
                    mindiff = diff
            i = i + 1

        # that means the ident (species) was not found
        if found == -1:
            print("ERROR: Could not find any line estimates for ident: ", ident)
            return None

        if self.lineEstimates[found].rInfo is None:
            _read_lineEstimateRinfo(self, self.lineEstimates[found])

        return self.lineEstimates[found]

    def selectLineEstimates(
        self, ident: str | None, wlrange: list[float, float] | None = None
    ) -> list[DataLineEstimate]:
        """
        Returns a list of all line estimates (i.e. all transitions) for the
        given line ident and/or in the given wavelength range.

        Parameters
        ----------
        ident :
          The line identification (species name) as defined in |prodimo|.
          The ident is not necessarily equal to the underlying chemical species
          name (e.g. isotopologues, ortho-para, or cases like N2H+ and HN2+).
          If ``wlrange`` is set ident can be ``None`` in that case all lines in the given
          wavelength range are returned.

        wlrange : All lines in the given wavelength range [start,end] and the given ident
          are returned. if the ident is `None` all lines are returned.
          Default: `None` Units: micron

        Returns
        -------
        list(:class:`prodimopy.read.DataLineEstimate`) :
          List of :class:`prodimopy.read.DataLineEstimate` objects, or empty list if nothing was found.

        Notes
        -----
        In this routine the additional radial information of the line estimate
        (see :class:`~prodimopy.read.DataLineEstimateRInfo`) is not read.

        Examples
        --------

        .. code-block:: python

          # select all line estimates for CO
          lests=model.selectLineEstimates("CO")

          # select only the 1300 micron CO line
          lests=model.selectLineEstimates("CO",wlrange=[1300,1310])

          # select all linest in the given wavelength range
          lests=model.selectLineEstimates(None,wlrange=[1200,1400])

          # print all of them to see what we got
          for lest in lests:
            print(lest)

        """
        assert self.lineEstimates is not None

        lines = list()
        if wlrange is None:
            for le in self.lineEstimates:
                if le.ident == ident:
                    lines.append(le)
        else:
            # TODO: maybe this can be done better/faster
            for le in self.lineEstimates:
                if le.wl >= wlrange[0] and le.wl <= wlrange[1]:
                    if ident is None or le.ident == ident:
                        lines.append(le)

        if len(lines) == 0:
            print("ERROR: Could not find any line estimates ...")

        return lines

    def getLineOriginMask(self, lineEstimate: DataLineEstimate) -> NDArray[np.float64]:
        """
        Returns a numpy mask where the grid points outside the emission
        origin area for the given ``lineEstimate`` are marked as invalid.

        This mask can be used in e.g. :func:`~prodimopy.read.Data_ProDiMo.avg_quantity`

        Parameters
        ----------
        lineEstimate :
          A line estimate object for which the mask should be created.

        Returns
        -------
        NDArray[np.float64]
          Numpy mask with *DIMS:* (nx,nz)
        """
        fcfluxes = np.array([x.Fcolumn for x in lineEstimate.rInfo])

        Fcum = fcfluxes[:]
        for i in range(1, self.nx):
            Fcum[i] = Fcum[i - 1] + fcfluxes[i]

        interx = interp1d(Fcum / Fcum[-1], self.x[:, 0])
        x15 = interx(0.15)
        x85 = interx(0.85)

        mask = np.ones(shape=(self.nx, self.nz))
        for ix in range(self.nx):
            if self.x[ix, 0] >= x15 and self.x[ix, 0] <= x85:
                for iz in range(self.nz):
                    rinfo = lineEstimate.rInfo[ix]
                    # print(rinfo.z15,rinfo.z85)
                    if self.z[ix, iz] <= rinfo.z15 and self.z[ix, iz] >= rinfo.z85:
                        mask[ix, iz] = 0

        return mask

    def getAbun(self, spname):
        """
        Returns the abundance for a given species.

        Parameters
        ----------
        spname : string
          The name of the chemical species as define in |prodimo|.

        Returns
        -------
        array_like(float,ndim=2)
          an array of dimension [nx,nz] with species abundance or `None` if the species was not found.

        Notes
        -----
          The abundance is given relative to the total hydrogen nuclei density
          (i.e. ``nmol(spname)/nHtot``)

          A warning is printed in case the species was not found in spnames.
        """

        if spname not in self.spnames:
            print("WARN: getAbun: Species " + spname + " not found.")
            return None

        return self.nmol[:, :, self.spnames[spname]] / self.nHtot

    def get_TotSpeciesMass(self, spname=None):
        """
        Returns the total mass (integrated over the whole disk) for all or one given species.

        The total mass is calculated by summing up the product of the number density and the volume
        at each grid point and multiplying it with the mass of one molecule.
        A warning is printed in case the species was not found in spnames.

        Parameters
        ----------
        spname : string
          The name of the chemical species as defined in |prodimo|.
          If `None` an array with the species masses of all elements will be returned.

        Returns
        -------
        float or array_like(float)
          The total mass of the species in grams or an array with the masses of all species.
          `None` if the species was not found.

        """

        def tmass(spec, model):
            return np.sum(
                model.vol * (model.nmol[:, :, model.spnames[spec]] * model.species.mass[spec])
            )

        if spname is None:
            all = list()
            for spname in self.spnames:
                all.append(tmass(spname, self))
            return np.array(all)

        else:
            if spname not in self.spnames:
                print("WARN: getTotSpeciesMass: Species " + spname + " not found.")
                return None

            return tmass(spname, self)

    def get_toomreQ(self, mstar=None):
        """
        Returns the Toomre Q parameter as a function of radius.
        (for the midplane).

        Q is given by

        Q(r)=k(r)*cs(r)/(pi * G * sigma(r))

        for k we use the keplerian frequency, cs is the soundspeed (from the mdoel)
        and sigma is the total gas surface density (both half's of the disk).

        Parameters
        ----------
        mstar : float
          The stellar mass in solar units (optional).
          If `None` the value from the model is taken.

        Returns
        -------
        array_like(float,ndim=1)
          an array of dimension [nx] with the Q param
        """
        if mstar is None:
            mstar = self.mstar

        mstarc = (mstar * u.M_sun).cgs.value
        grav = const.G.cgs.value
        r = (self.x[:, 0] * u.au).cgs.value
        # isothermal soundspeed
        cs = (self.soundspeed[:, 0] * u.km / u.s).cgs.value
        # surface density factor two for both half of the disks
        sigma = 2.0 * (self.sdg[:, 0] * u.g / u.cm**2).cgs.value

        # assume Keplerian rotation for Epicyclic frequency
        kappa = np.sqrt(grav * mstarc / r**3)
        Q = kappa * cs / (math.pi * grav * sigma)

        return Q

    def get_VKep(self, mstar=None, type=2):
        """
        Returns the Keplerian rotation velocity [km/s] as a function
        of radius and height (same as in |prodimo|)


        Type 1: vkep=sqrt((G* mstar) / r)
        Type 2: vkep=sqrt((G* mstar * x**2) / r**3)
        Type 3: with pressure gradient (see Rosenfeld+ 2013)

        Parameters
        ----------
        mstar : float
          The stellar mass in solar units (optional).
          If `None` the value from the model is taken.

        Returns
        -------
        array_like(float,ndim=1)
          Rotation velocity [km/s]
        """
        if mstar is None:
            mstar = self.mstar

        mstarc = (mstar * u.M_sun).cgs.value
        grav = const.G.cgs.value

        tocm = ((1 * u.au).to(u.cm)).value
        r = np.sqrt(self.x**2 + self.z**2) * tocm

        if type == 1:
            # FIXME: Should be radius, but to be consistent do it like this.
            # but check again
            vkep = np.sqrt(grav * mstarc / (self.x * tocm))
        else:
            vrot2 = (grav * mstarc * (self.x * tocm) ** 2) / r**3

            if type == 2:  # standard in ProDiMo
                vkep = np.sqrt(vrot2)
            elif type == 3:  # include the pressure term
                # pressuregradient like Rosenfeld+ 2013
                dp = self.x * 0.0
                for iz in range(self.nz):
                    # this is used in e.g. Rosenfeld et al 2013 and others
                    dp[:, iz] = np.gradient(self.pressure[:, iz], self.x[:, iz] * tocm)
                    # this we use in ProDiMo currently I think that is correct
                    # doesn't seem to much of a difference
                    # dp[:,iz]=np.gradient(self.pressure[:,iz],r[:,iz])
                vkep = np.sqrt(vrot2 + (self.x * tocm) / self.rhog * dp)
            else:
                vkep = np.sqrt(vrot2)

        vkep = ((vkep * u.cm / u.s).to(u.km / u.s)).value
        return vkep

    def get_KeplerOmega(self, mstar=None):
        """
        Returns the Keplerian orbital frequency [1/s]
        (for the midplane).

        omega=sqrt(G*mstar/r**3)

        Parameters
        ----------
        mstar : float
          The stellar mass in solar units (optional).
          If `None` the value from the model is taken.

        Returns
        -------
        array_like(float,ndim=1)
          Keplerian orbital frequency as function of radius [1/s]
        """
        if mstar is None:
            mstar = self.mstar

        mstarc = (mstar * u.M_sun).cgs.value
        grav = const.G.cgs.value
        r = (self.x[:, 0] * u.au).cgs.value

        # assume keplerian rotation for Epicyclic frequency
        omega = np.sqrt(grav * mstarc / r**3)

        return omega

    def int_ring(self, quantity, r1=None, r2=None):
        """
        Integrates the given quantity (needs to be a function of r) from
        rin to rout.

        No interpolation is done. Simply the nearest neighbour for rin and rout
        are taken.

        The integration is done in cgs units and also the return value is in cgs units.

        For example if the total gas surface density is passed this routine gives the disk mass.
        (if r1=rin and r2=rout).

        Parameters
        ----------
        quantity : array_like(float,ndim=1)
          the quantity to average. *DIMS:* (nx).
        r1: float
          inner radius [au].
          optional DEFAULT: inner disk radius
        r2: float
          inner radius [au].
          optional DEFAULT: outer disk radius
        """

        if r1 is None:
            r1idx = 0
        else:
            r1idx = np.argmin(np.abs(self.x[:, 0] - r1))

        if r2 is None:
            r2idx = self.nx - 1
        else:
            r2idx = np.argmin(np.abs(self.x[:, 0] - r2))

        print(
            "INFO: Integrate from "
            + "{:8.4f} ({:4d})".format(self.x[r1idx, 0], r1idx)
            + " au to "
            + "{:8.4f} ({:4d})".format(self.x[r2idx, 0], r2idx)
            + " au"
        )

        r = (self.x[:, 0] * u.au).to(u.cm).value
        out = (
            2.0
            * math.pi
            * integrate.trapezoid(
                quantity[r1idx : r2idx + 1] * r[r1idx : r2idx + 1], x=r[r1idx : r2idx + 1]
            )
        )

        return out

    def avg_quantity(self, quantity, weight="gmass", weightArray=None, mask=None):
        """
        Calculates the weighted mean value for the given field (e.g. td).
        Different weights can be used (see `weight` parameter)

        Parameters
        ----------
        quantity : array_like(float,ndim=2)
          the quantity to average. *DIMS:* (nx,nz).

        weight : str
          option for the weight. Values: `gmass` (gas mass) `dmass` (dust mass) or
          `vol` (Volume). DEFAULT: `gmass`

        weightArray : array_like(float,ndim=2)
          Same dimension as `quantity`. If `weightArray` is not `None` it is used
          as the weight for calculating the mean value.

        mask : array_like(boolean,ndim=2)
          A mask with the same dimension as `quantity`. All elements with `True` are
          masked, i.e. not considered in the average (see numpy masked_array).
          For example one can pass the result of :meth:`~prodimopy.read.getLineOriginMask`
          to calculate average quantities over the emitting region of a line.


        Examples
        --------

        Here is an example for making a mass weighted average for the gas temperature in the main
        line emitting region for the CO 1.3 mm line.  `model` is the model data read with
        :func:`~prodimopy.read.read_prodimo`.

        .. code-block:: python

          avgtg=model.avg_quantity(model.tg,weight="gmass",
                            mask=model.getLineOriginMask(model.getLineEstimate("CO",1300.)))

        """
        vol = np.ma.masked_array(self.vol, mask=mask)
        quantitym = np.ma.masked_array(quantity, mask=mask)

        if weightArray is not None:
            wA = np.ma.masked_array(weightArray, mask=mask)
            mean = np.sum(np.multiply(wA, quantitym))
            return mean / np.sum(wA)
        else:
            if weight == "vol":
                mean = np.sum(np.multiply(vol, quantitym))
                return mean / np.sum(vol)
            else:
                if weight == "dmass":
                    rho = np.ma.masked_array(self.rhod, mask=mask)
                else:
                    rho = np.ma.masked_array(self.rhog, mask=mask)

                mass = np.multiply(vol, rho)
                mean = np.sum(np.multiply(mass, quantitym))
                mean = mean / np.sum(mass)
                return mean

    def analyse_chemistry(
        self,
        species: str,
        to_txt: bool = True,
        filenameChemistry: str = "chemanalysis.out",
        screenout: bool = False,
    ) -> Chemistry:
        """
        Routine to create a Chemistry analysis object for the given species, if the chemanalysis data is available.

        Parameters
        ----------
        species :
          The species to analyse.
        to_txt :
          Write info about formation and destruction reactions for the selected molecule to a txt file.
        filenameChemistry :
          The name of the file that holds the reaction rates. Just in case it has a different name, usually one does not need to change that.
        screenout :
          If ``True`` all the form./dest. reactions are  printed on the screen.

        Returns
        -------
        Chemistry :
          Object that holds all the required information and can be use for the plotting routines or for :func:`~prodimopy.read.reac_rates_ix_iz`.

        """
        import astropy.io.fits as fits

        chemistry = Chemistry(self.name)

        start = timer()

        # stores all the formation reaction indices and rates for each grid point
        gridf = np.empty((self.nx, self.nz, 2), dtype=np.ndarray)
        gridd = np.empty((self.nx, self.nz, 2), dtype=np.ndarray)
        totfrate = np.zeros((self.nx, self.nz))  # total formation rate at each point)
        totdrate = np.zeros((self.nx, self.nz))  # total formation rate at each point)
        fidx = list()  # indices of all unique formation reactions
        didx = list()  # indices of all unique destruction reactions

        # check if already a fits file with the given.out name exits
        fnamefits = filenameChemistry.replace(".out", ".fits")
        if self.td_fileIdx is not None:  # take the time-dependent file index from the model
            ext = _td_fileIdx_ext(self.td_fileIdx)
            fnamefits = fnamefits.replace(".fits", ext + ".fits")

        if os.path.isfile(os.path.join(self.directory, fnamefits)):
            # if so, use it
            print("INFO: Using existing fits file for chemanalysis: ", fnamefits)
            filenameChemistry = fnamefits
        else:
            print("INFO: convert existing txt format file to fits (that can take a bit) ... ")
            # create an array that holds the reaction rates
            rates = np.zeros(
                shape=(self.nx, self.nz, len(self.chemnet.reactions)), dtype=np.float32
            )
            if self.td_fileIdx is not None:
                # if it is a time-dependent model, the filenameChemistry is different
                # not nice, but ext should be set already
                filenameChemistry = filenameChemistry.replace(".out", ext + ".out")
            fc = open(os.path.join(self.directory, filenameChemistry), "r")

            fc.readline()  # skip the first line
            for line in fc:
                ix, iz, dummy, ireac, rate = line.split()
                rates[int(ix) - 1, int(iz) - 1, int(ireac) - 1] = float(rate)

            fc.close()
            hdu = fits.PrimaryHDU(
                data=rates.T
            )  # transpose to have it in the same order as it would be from prodimo
            hdu.writeto(os.path.join(self.directory, fnamefits), overwrite=True)
            filenameChemistry = fnamefits

        # that gives me simply all formation and destruction reactions for the given species

        # those include the real ids (e.g. starts at 1) and not the zero-based python indices!!
        fidx = np.array([x.id for x in self.chemnet.reactions if species in x.products])
        didx = np.array([x.id for x in self.chemnet.reactions if species in x.reactants])

        # now read all info from the fits file
        cfits = fits.open(
            os.path.join(self.directory, filenameChemistry),
            do_not_scale_image_data=True,
            memmap=True,
        )
        formrates = cfits[0].data[fidx - 1, :, :]  # is read in reversed order for the dims
        destrates = cfits[0].data[didx - 1, :, :]
        formrates = formrates.T  # transpose it to have it in nx,nz,ncreac ...
        destrates = destrates.T  # transpose it to have it in nx,nz,ncreac ...
        cfits.close()

        # sorted indices for the formation and destruction rates
        formridx = np.flip(np.argsort(formrates, axis=2), axis=2)  # reversed order
        destridx = np.flip(np.argsort(destrates, axis=2), axis=2)  # reversed order

        for ix in range(self.nx):
            for iz in range(self.nz):
                gridf[ix, iz, 0] = fidx[formridx[ix, iz, :]]  # formation reaction indices, sorted
                gridf[ix, iz, 1] = formrates[ix, iz, formridx[ix, iz, :]]
                gridd[ix, iz, 0] = didx[
                    destridx[ix, iz, :]
                ]  # destruction reaction indices, sorted
                gridd[ix, iz, 1] = destrates[ix, iz, destridx[ix, iz, :]]

        totfrate[:, :] = np.sum(formrates, axis=2)  # total formation rate at each point
        totdrate[:, :] = np.sum(destrates, axis=2)  # total destruction rate at each point

        chemistry.species = species
        chemistry.gridf = gridf
        chemistry.gridd = gridd
        chemistry.fridxs = fidx
        chemistry.dridxs = didx
        chemistry.totfrate = totfrate
        chemistry.totdrate = totdrate
        chemistry.model = self  # reference to the underlying model

        if to_txt:
            output_chem_fname = os.path.join(
                self.directory, "chemistry_reactions_" + species + ".txt"
            )
            if self.td_fileIdx is not None:
                output_chem_fname = output_chem_fname.replace(".txt", ext + ".txt")
            f = open(output_chem_fname, "w")
            f.writelines("-------------------------------------------------------\n")
            f.writelines("formation and destruction reactions \n")
            f.writelines("species: " + species + "\n\n")
            f.writelines("Formation reactions\n")
            for i, ridx in enumerate(chemistry.fridxs):
                f.writelines(chemistry.reac_to_str(self.chemnet.reactions[ridx - 1], i + 1))
                f.writelines("\n")
            f.writelines("\n\n")
            f.writelines("Destruction reactions\n")
            for i, ridx in enumerate(chemistry.dridxs):
                f.writelines(chemistry.reac_to_str(self.chemnet.reactions[ridx - 1], i + 1))
                f.writelines("\n")
            f.writelines("-------------------------------------------------------\n")
            f.close()
            print("INFO: Writing information to: " + output_chem_fname)

            # also print it to stdout
            if screenout:
                with open(output_chem_fname) as f:
                    print(f.read())

        print(
            f"INFO: Found {len(chemistry.fridxs)} formation and {len(chemistry.dridxs)} destruction reactions for species {species}."
        )
        print("INFO: Calc time: ", "{:4.2f}".format(timer() - start) + " s")
        print("")
        return chemistry

    def freezeout_timescale(self, species, alpha=1.0):
        """
        Calculates the freezeout timescale for the given species, on the full grid using
        Eq. 12 from `Rab+ (2017) <https://ui.adsabs.harvard.edu/abs/2017A%26A...604A..15R/abstract>`_ .

        Parameters
        ----------
        species : string
          The chemical species for which the freezeout timescale should be calculated.

        alpha : float
          The sticking coefficient. Default: 1.0

        Returns
        -------
        array_like(float,ndim=2)
          The freezeout timescale for the given species in years. *DIMS:* (nx,nz)

        .. todo::

          - get sticking coefficient from parameter file. However, that might not be possible
            if an equation is used.

        """
        mw = (self.species.mass[species] * u.g) / (1.0 * u.u).cgs
        rhodp = self.p_rho_grain

        return (
            2.9e-12
            * mw.value**0.5
            * 1.0
            / alpha
            * rhodp
            / self.d2g
            * self.tg ** (-0.5)
            * self.da2mean
            * 1.0
            / self.rhog
        )


def read_prodimo(
    directory=".",
    name=None,
    readlineEstimates=True,
    readObs=True,
    readImages=True,
    filename="ProDiMo.out",
    filenameLineEstimates="FlineEstimates.out",
    filenameLineFlux="line_flux.out",
    filenameFLiTs="specFLiTs.out",
    td_fileIdx: str | int = None,
):
    """
    Reads in all (not all yet) the output of a |prodimo| model from the given model directory.

    Parameters
    ----------
    directory : str
      the directory of the model (optional). One can use `~` for the home directory
    name : str
      an optional name for the model (e.g. can be used in the plotting routines)
    readlineEstimates : boolean
      read the line estimates file (can be slow, so it is possible to deactivate it)
    readObs : boolean
      try to read observational data (e.g. SEDobs.dat ...)
    filename : str
      the filename of the main prodimo output
    filenameLineEstimates : str
      the filename of the line estimates output
    filenameLineFlux : str
      the filename of the line flux output
    filenameFLiTs : str
      the filename of the flits output
    td_fileIdx :
      in case of time-dependent model the index of a particular output age can be provided (e.g. "03")
      if it is an int try to expand the index properly to a string (currently 1 becomes "0001")

    Returns
    -------
    :class:`prodimopy.read.Data_ProDiMo`
      the |prodimo| model data or `None` in case of errors.
    """

    startAll = timer()

    if directory.startswith("~"):
        directory = os.path.expanduser(directory)

    # guess a name if not set
    if name is None:
        if directory is None or directory == "." or directory == "":
            dirfields = os.getcwd().split("/")
        else:
            dirfields = directory.split("/")

        if dirfields[-1] == "":  # this is the case for path/
            name = dirfields[-2]
        else:
            name = dirfields[-1]

    data = Data_ProDiMo(name)
    
    # Reads StarSpecrum.out 
    data.star = read_star(directory)
    if data.star is not None:
        data.lambs=data.star._lambs # can be None, but if RTinterpolation.out exists we can get it
    else:
        data.lambs=None

    # if td_fileIdx is given alter the filenames so that the time-dependent
    # files can be read. However this would actually also work with other kind
    # of indices as td_fileIdx can be a string
    if td_fileIdx is not None:
        rpstr = _td_fileIdx_ext(td_fileIdx)
        filename = filename.replace(".out", rpstr + ".out")
        filenameLineEstimates = filenameLineEstimates.replace(".out", rpstr + ".out")
        filenameLineFlux = filenameLineFlux.replace(".out", rpstr + ".out")
        filenameFLiTs = filenameFLiTs.replace(".out", rpstr + ".out")

    f, dummy = _getfile(filename, directory, suppressMsg=True)

    # need to stop, means no ProDiMo.out, message is printed in getfiles
    if f is None:
        raise FileNotFoundError("ERROR: Could not read "+os.path.join(directory,filename))

    # read all data into the memory; easier to handle afterwards
    lines = f.readlines()
    f.close()

    # start of the array data block
    idata = 24

    # store the file idx for later use. That should work, even if it is a string, if not we have bigger problems.
    if td_fileIdx is not None:
        data.td_fileIdx = int(td_fileIdx)
    else:
        data.td_fileIdx = None

    data.directory = directory
    # Read first the species, because only from there I can know if the electron
    # is included as Species or not
    # data is filled in the routine
    data.species = read_species(directory)
    if data.species is not None:  # None should not happen
        data.nspec = len(data.species.mass)

    # This can happen if there is not StarSpectrum.out. But we want to read the ProDiMo.out, anyway.
    if data.star is None:
        data.star = DataStar(0, 0, 0, 0, 0)

    data.star.mass = float(lines[0].split()[1])
    data.star.Lstar = float(lines[1].split()[1])

    data.p_mdisk = float(lines[5].split()[1])
    data.p_dust_to_gas = float(lines[9].split()[1])
    data.p_rho_grain = float(lines[10].split()[1])
    data.p_v_turb = float(lines[18].split()[1])

    strs = lines[21].split()
    data.nx = int(strs[1])
    data.nz = int(strs[2])
    # is not set in read_species() FIXME: not nice
    nspecreal = int(strs[3])
    if data.nspec is None:  # should not happen
        print("WARN: Setting data.nspec, because there is no Species.out")
        data.nspec = nspecreal + 1  # +1 for the electron
    data.nheat = int(strs[4])
    data.ncool = int(strs[5])
    data.nlam = int(strs[6])

    # move this to the constructor which takes nx,nz
    data.x = np.zeros(shape=(data.nx, data.nz))
    data.z = np.zeros(shape=(data.nx, data.nz))
    data.lams = np.zeros(shape=(data.nlam))
    data.AV = np.zeros(shape=(data.nx, data.nz))
    data.AVrad = np.zeros(shape=(data.nx, data.nz))
    data.AVver = np.zeros(shape=(data.nx, data.nz))
    data.NHver = np.zeros(shape=(data.nx, data.nz))
    data.NHrad = np.zeros(shape=(data.nx, data.nz))
    data.d2g = np.zeros(shape=(data.nx, data.nz))
    data.tg = np.zeros(shape=(data.nx, data.nz))
    data.td = np.zeros(shape=(data.nx, data.nz))
    data.nd = np.zeros(shape=(data.nx, data.nz))
    data.soundspeed = np.zeros(shape=(data.nx, data.nz))
    data.rhog = np.zeros(shape=(data.nx, data.nz))
    data.pressure = np.zeros(shape=(data.nx, data.nz))
    data.solved_chem = np.zeros(shape=(data.nx, data.nz), dtype=np.int32)
    data.tauchem = np.zeros(shape=(data.nx, data.nz))
    data.taucool = np.zeros(shape=(data.nx, data.nz))
    data.taudiff = np.zeros(shape=(data.nx, data.nz))
    data.heat_mainidx = np.zeros(shape=(data.nx, data.nz), dtype=np.int32)
    data.cool_mainidx = np.zeros(shape=(data.nx, data.nz), dtype=np.int32)
    data.nHtot = np.zeros(shape=(data.nx, data.nz))
    data.damean = np.zeros(shape=(data.nx, data.nz))
    data.Hx = np.zeros(shape=(data.nx, data.nz))
    data.tauX1 = np.zeros(shape=(data.nx, data.nz))
    data.tauX5 = np.zeros(shape=(data.nx, data.nz))
    data.tauX10 = np.zeros(shape=(data.nx, data.nz))
    data.zetaX = np.zeros(shape=(data.nx, data.nz))
    data.chi = np.zeros(shape=(data.nx, data.nz))
    data.chiRT = np.zeros(shape=(data.nx, data.nz))
    data.kappaRoss = np.zeros(shape=(data.nx, data.nz))
    data.zetaCR = np.zeros(shape=(data.nx, data.nz))
    data.zetaSTCR = np.zeros(shape=(data.nx, data.nz))
    data.da2mean = np.zeros(shape=(data.nx, data.nz))
    data.dNlayers = np.zeros(shape=(data.nx, data.nz))
    data.velocity = np.zeros(shape=(data.nx, data.nz, 3))

    data.heat_names = list()
    data.cool_names = list()
    data.rateH2form = np.zeros(shape=(data.nx, data.nz))
    data.rateH2diss = np.zeros(shape=(data.nx, data.nz, 3))

    # init the caches, to avoid conversion to float if not necessary
    # Item size (S13) is required, 13 should be enough
    data._radFields_cache = np.empty((data.nx, data.nz, data.nlam), dtype="S13")
    data._nmol_cache = np.empty((data.nx, data.nz, data.nspec), dtype="S13")
    data._heat_cache = np.empty((data.nx, data.nz, data.nheat), dtype="S13")
    data._cool_cache = np.empty((data.nx, data.nz, data.ncool), dtype="S13")

    # Make some checks for the format
    # new EXP format for x and z:
    newexpformat = lines[idata].find("E", 0, 25) >= 0  # type: ignore
    # number of fixed fields in ProDiMo.out (before heating and cooling rates)
    nfixFields = 21

    # index after the J data/fields in ProDiMo
    iACool = nfixFields + data.nheat + data.ncool
    iASpec = iACool + 1 + data.nspec

    # this means the e- is also included as a species, it is then also included
    # in the output as the last element, simply skip that column then.
    # in prodimopy e- was anyway treated as a species.
    iASpecskip = 0
    if nspecreal == data.nspec:
        iASpecskip = 1

    iAJJ = iASpec + iASpecskip + data.nlam

    # read the species names, these are taken from the column titles
    colnames = lines[idata - 1]

    # FIXME: Again hardcoding. Might be better to read the Species names
    # from Species.out. Assumes that the name for each species has len 13.
    # Assume that the first species is e- and search for that
    # that is more flexible in case other names change
    # specStart = 233 + data.nheat * 13 + data.ncool * 13 + 13
    # do not include the electron in the splitting because that one is special
    specStart = colnames.find("           e-") + 13
    # Deal with e- as species (el_is_sp=true), in that
    # case it is included twice in the output but using nspec from ProDiMo.out
    # should be fine (i.e. ignore the last column of the species which is then e- again).
    spnames = colnames[specStart : specStart + (data.nspec - 1) * 13].split()
    # now insert the electron again.
    # but both are dictionaries so I guess it should be fine
    spnames.insert(0, "e-")  # type: ignore
    if len(spnames) != data.nspec:
        print("ERROR: something is wrong with the number of Species!")
        return None

    # empty dictionary
    data.spnames = OrderedDict()
    # Make a dictionary for the spnames
    for i in range(data.nspec):
        data.spnames[str(spnames[i])] = i

    # read the heating and cooling names
    iheat = idata + data.nx * data.nz + 2
    for i in range(data.nheat):
        data.heat_names.append(lines[iheat + i][3:].strip())

    icool = idata + data.nx * data.nz + 2 + data.nheat + 2
    for i in range(data.ncool):
        data.cool_names.append(lines[icool + i][3:].strip())

    # read the band wavelenghts
    iwls = idata + data.nx * data.nz + 2 + data.nheat + 2 + data.ncool + 2
    for i in range(data.nlam):
        data.lams[i] = float((lines[iwls + i].split())[1])

    i = 0

    # startLoop=timer()
    with tqdm(total=data.nz * data.nx, desc=f"READ: {filename}: ") as pbar:
        for iz in range(data.nz):
            zidx = data.nz - iz - 1
            for ix in range(data.nx):
                pbar.update(1)
                # stupid workaround for big disks/envelopes where x,y can be larger than 10000 au
                # there is no space between the numbers for x and z so always add one if none is there
                # this might can be removed in the future as the newest ProDiMo version use exp format now
                line = lines[idata + i]
                if not newexpformat:
                    if line[20] != " ":
                        line = line[:20] + " " + line[20:]  # type: ignore
                    # needs another fix
                    if line[8] != " ":
                        line = line[:8] + " " + line[8:]  # type: ignore

                # This line is what eats the time, but using genfromtxt for the ProDiMo.out
                # does not seem to be faster
                # fields=np.fromstring(line,sep=" ")
                fields = line.split()

                data.x[ix, zidx] = fields[2]
                data.z[ix, zidx] = fields[3]
                data.NHrad[ix, zidx] = fields[4]
                data.NHver[ix, zidx] = fields[5]
                data.AVrad[ix, zidx] = fields[6]
                data.AVver[ix, zidx] = fields[7]
                data.nd[ix, zidx] = fields[8]
                data.tg[ix, zidx] = fields[9]
                data.td[ix, zidx] = fields[10]
                data.soundspeed[ix, zidx] = fields[11]
                data.rhog[ix, zidx] = fields[12]
                data.pressure[ix, zidx] = fields[13]
                data.solved_chem[ix, zidx] = fields[14]
                data.chi[ix, zidx] = fields[15]
                data.tauchem[ix, zidx] = fields[16]
                data.taucool[ix, zidx] = fields[17]
                data.taudiff[ix, zidx] = fields[18]
                data.heat_mainidx[ix, zidx] = fields[19]
                data.cool_mainidx[ix, zidx] = fields[20]
                data._heat_cache[ix, zidx, :] = fields[nfixFields : nfixFields + data.nheat]
                data._cool_cache[ix, zidx, :] = fields[
                    (nfixFields + data.nheat) : (nfixFields + data.nheat + data.ncool)
                ]
                data.nHtot[ix, zidx] = fields[iACool]
                data._nmol_cache[ix, zidx, :] = fields[iACool + 1 : iASpec]
                data._radFields_cache[ix, zidx, :] = fields[(iASpec + iASpecskip) : iAJJ]
                data.chiRT[ix, zidx] = fields[iAJJ]
                data.kappaRoss[ix, zidx] = fields[iAJJ + 1]
                data.damean[ix, zidx] = fields[iAJJ + 3]
                data.d2g[ix, zidx] = fields[iAJJ + 4]
                data.Hx[ix, zidx] = fields[iAJJ + 5]
                data.tauX1[ix, zidx] = fields[iAJJ + 6]
                data.tauX5[ix, zidx] = fields[iAJJ + 7]
                data.tauX10[ix, zidx] = fields[iAJJ + 8]
                data.zetaX[ix, zidx] = fields[iAJJ + 9]
                data.rateH2form[ix, zidx] = fields[iAJJ + 10]
                data.rateH2diss[ix, zidx, :] = fields[iAJJ + 11 : iAJJ + 11 + 3]
                data.zetaCR[ix, zidx] = fields[iAJJ + 16]
                if len(fields) > (iAJJ + 17):
                    data.zetaSTCR[ix, zidx] = fields[iAJJ + 17]
                    if len(fields) > (iAJJ + 18):
                        data.da2mean[ix, zidx] = fields[iAJJ + 18]
                        # it seems Nlayers can sometimes become crazy numbers then e.g +100 is in the file without an e
                        data.dNlayers = _convToFloatCheck(fields[iAJJ + 19], ix, zidx, "dNlayers")

                        if len(fields) > (iAJJ + 20):
                            data.velocity[ix, zidx, :] = fields[iAJJ + 20 : iAJJ + 23]
                        else:
                            data.velocity = None  # for backward compatibilit, as it is a new field

                    else:
                        data.velocity = None  # for backward compatibilit, as it is a new field
                        data.da2mean = None
                        data.dNlayers = None

                i = i + 1

    # endLoop=timer()

    # derived quantitites
    data.rhod = data.rhog * data.d2g

    # AV like defined in the prodimo idl script
    for ix in range(data.nx):
        for iz in range(data.nz):
            data.AV[ix, iz] = np.min(
                [
                    data.AVver[ix, iz],
                    data.AVrad[ix, iz],
                    data.AVrad[data.nx - 1, iz] - data.AVrad[ix, iz],
                ]
            )

    # Read FlineEstimates.out
    if readlineEstimates:
        read_lineEstimates(directory, data, filename=filenameLineEstimates)
    else:
        data.lineEstimates = None

    data.elements = read_elements(directory)

    data.dust = read_dust(directory)

    fileloc = directory + "/dust_opac_env.out"
    if os.path.isfile(fileloc):
        data.env_dust = read_dust(directory, filename="dust_opac_env.out")

    if os.path.exists(directory + "/gas_cs.out"):
        data.gas = read_gas(directory)        
        if (data.lambs is None):
        # quick hack to fill lambs, the grid is taken for gas_cs_band.out, if we don't have it already            
            fbandgas=os.path.join(directory ,"gas_cs_band.out")
            if os.path.exists(fbandgas):
                vals=np.loadtxt(fbandgas,comments="#",skiprows=2,usecols=(0,))
                # just get the edges, last one needs to be added by hand
                data.lambs=vals[0::3]
                data.lambs=np.append(data.lambs,vals[-1])            


    if os.path.exists(directory + "/" + filenameLineFlux):
        data.lines = read_linefluxes(directory, filename=filenameLineFlux)

    if os.path.exists(directory + "/SED.out"):
        data.sed = read_sed(directory)

    if readObs:
        data.sedObs = read_continuumObs(directory)
        if data.lines is not None:
            if os.path.exists(directory + "/LINEobs.dat"):
                data.lineObs = read_lineObs(directory, len(data.lines))

            # FIXME: workaround set also the frequency for the observed lline
            if data.lineObs is not None:
                for i in range(len(data.lines)):
                    data.lineObs[i].frequency = data.lines[i].frequency
                    if data.lineObs[i].profile is not None:
                        data.lineObs[i].profile.restfrequency = data.lineObs[i].frequency

    if readImages:
        data.contImages = read_continuumImages(directory)
        # FIXME: not very nice, if one calls the routine directly the inclinations will not be set
        if data.contImages is not None:
            data.contImages._inclinations = data.sed._inclinations

    if os.path.exists(directory + "/" + filenameFLiTs):
        data.FLiTsSpec = read_FLiTs(directory, filenameFLiTs)

    if os.path.exists(directory + "/Parameter.out"):
        data.params = ModelParameters(filename="Parameter.out", directory=directory)
        # Also set the age of the model if it is a time-dependent model
        if data.td_fileIdx is not None:
            data.age = data.params["AGE_DISK"][data.td_fileIdx - 1]
        else:
            data.age = np.inf  # steady state model

    # Try to read some special files
    _read_12CO13CO_ratio(data)

    # print("INFO: Loop time: ","{:4.2f}".format(endLoop-startLoop)+" s")
    print("INFO: Reading time: ", "{:4.2f}".format(timer() - startAll) + " s")

    # set muH
    data.muH = data.rhog[0, 0] / data.nHtot[0, 0]

    print(" ")

    return data


def _convToFloatCheck(valstr: str, ix: int, iz: int, fieldname: str) -> float:
    """
    Converts a string to a float but catches ValueErrors and deals with it.

    Catches the case with wrong exponentail format eg. 1.0089+100 that can happen
    in |prodimo| output files. It should not happen, but this as a good workaround to
    still be able to read the data.

    Parameters:
    -----------
    valstr : str
      the string to convert

    ix : int
      the x index (just for error message)

    iz : int
      the z index (just for error message)

    fieldname : str
      the name of the field (as e.g. in the ProDiMo.out)

    """
    try:
        val = float(valstr)
    except ValueError as e:
        if "+" in valstr:
            val = 1.0e99  # assumes a large number
        elif "-" in valstr:
            val = 1.0e-99  # assumes a very small number
        else:
            val = np.nan
        print(f"WARN: Could not convert {fieldname} at ix={ix}, iz={iz}, (E: {e}) set it to {val}")
    return val


def _td_fileIdx_ext(td_fileIdx: str | int) -> str:
    """
    Returns the extension for the time-dependent file index.

    This should be used to build the filename for the time-dependent output files.


    Parameters
    ----------
    td_fileIdx : str or int
      the time-dependent file index, e.g. "03" or 3. If it is an `int` it will be formatted
      to a 4 digit string with leading zeros.

    Returns
    -------
    str :  the extension for the time-dependent file index, e.g. "_0003.out".


    """
    if td_fileIdx is not None:
        if isinstance(td_fileIdx, int):
            td_fileIdx = "{:04d}".format(td_fileIdx)
        return "_" + td_fileIdx
    else:
        return ""


def read_elements(directory, filename="Elements.out"):
    """
    Reads the Elements.out file.
    Also adds the electron "e-" to the Elements.

    Parameters
    ----------
    directory : str
      the directory of the model

    filename: str
      an alternative Filename

    Returns
    -------
    :class:`~prodimopy.read.DataElements`
      the Elements model data or `None` in case of errors.

    """

    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    nelements = int(f.readline())

    elements = DataElements()
    f.readline()

    for i in range(nelements):
        line = f.readline()
        fields = line.strip().split()
        name = fields[0].strip()
        # FIXME: Workaround with the quadrupole solver an element ch is included
        # don't know what to do with that.
        if name == "ch":
            continue

        elements.abun12[name] = float(fields[1])
        elements.abun[name] = 10.0 ** (float(fields[1]) - 12.0)
        elements.amu[name] = float(fields[2])
        elements.massRatio[name] = float(fields[3])

    # also read muH (last element of the string)
    elements.muHamu = float(f.readline().strip().split()[-1])

    return elements


def read_species(directory, filename="Species.out") -> DataSpecies | None:
    """
    Reads the Species.out file.
    Also adds the electron "e-" if necessary.

    Also sets data.nspec as only here I can know if e- was a real species in
    |prodimo| or not. If it was a real species I don't need to add that.

    Parameters
    ----------
    directory : str
      the directory of the model

    pdata : :class:`prodimopy.read.Data_ProDiMo`
      the |prodimo| Model data structure, where the data is stored

    filename: str
      an alternative Filename

    Returns
    -------
    :class:`~prodimopy.read.DataSpecies`
      the Species model data or `None` in case of errors.

    ..todo :
      * stochiometry is still missing

    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    species = DataSpecies()

    # skip the first line
    f.readline()

    species.mass = OrderedDict()
    species.charge = OrderedDict()
    species.chemPot = OrderedDict()

    for line in f:
        fields = line.strip().split()
        spname = fields[2].strip()
        species.mass[spname] = (float(fields[3].strip()) * u.u).cgs.value
        species.charge[spname] = int(fields[4].strip())
        species.chemPot[spname] = float(fields[5].strip())

    # Only do this if it does not exist yet.
    # This is the only place where one can know if the e- is a real species
    # in ProDiMo or not (well could also use Parameter.out)
    if "e-" not in species.mass.keys():
        species.mass["e-"] = const.m_e.cgs.value
        species.charge["e-"] = -1
        species.chemPot["e-"] = 0.0
    else:
        # overwrite the mass, as it is not correct due to rounding in Species.out
        species.mass["e-"] = const.m_e.cgs.value

    # electron should be in first place like in ProDiMo.out
    species.mass.move_to_end("e-", last=False)
    species.charge.move_to_end("e-", last=False)
    species.chemPot.move_to_end("e-", last=False)

    return species


def read_lineEstimates(directory, pdata, filename="FlineEstimates.out"):
    """
    Read FlineEstimates.out Can only be done after |prodimo|.out is read.

    Parameters
    ----------
    directory : str
      the directory of the model

    pdata : :class:`prodimopy.read.Data_ProDiMo`
      the |prodimo| Model data structure, where the data is stored

    filename: str
      an alternative Filename

    """
    f, rfile = _getfile(filename, directory, binary=True, suppressMsg=True)
    if f is None:
        pdata.lineEstimates = None
        return None
    else:
        pdata.__fpFlineEstimates = rfile

    # check for version
    line = f.readline().decode()
    version = 1
    if len(line) > 68:
        # position of version
        posver = line.find("version")
        if posver >= 0:
            version = int(line[posver + len("version") :].strip())

    nlines = int(f.readline().strip())
    f.readline()

    pdata.lineEstimates = list()
    pdata.__versionFlineEstimates = version
    nxrange = list(range(pdata.nx))
    startBytes = 0

    for i in tqdm(range(nlines), f"READ: {filename}"):
        # has to be done in fixed format
        # It could be that nline is not really equal the number of available lines
        # this is might be a bug in ProDiMo but maybe intended (see
        # OUTPUT_FLINE_ESTIMATE in ProDiMo). Add a check to be sure
        line = f.readline()
        if not line:
            break

        line = line.decode()
        if version == 1:
            le = DataLineEstimate(
                (line[0:9]).strip(),
                float(line[10:28]),
                int(line[29:32]),
                int(line[33:37]),
                float(line[38:49]),
            )
        elif version == 2 or version == 3:
            try:
                le = DataLineEstimate(
                    (line[0:9]).strip(),
                    float(line[10:28]),
                    int(line[29:34]),
                    int(line[35:40]),
                    float(line[41:53]),
                )
            except ValueError as err:
                print("Conversion problems: {0}".format(err))
                print("Line (i,text): ", i, line)
                print("Field: ", line[0:9], line[10:28], line[29:34], line[35:40], line[41:53])
                raise err
        else:
            raise ValueError("Unknown version of FlineEstimates.out! version=" + str(version))

        # Find out the number of bytes in one radial line to use seek in the
        # next iterations
        if i == 0:
            start = f.tell()
            le.__posrInfo = start  # store the position for reading this info if required
            for j in nxrange:
                f.readline()
            startBytes = f.tell() - start
        else:
            le.__posrInfo = f.tell()
            f.seek(startBytes, 1)

        pdata.lineEstimates.append(le)

    f.close()


def _read_12CO13CO_ratio(pdata: Data_ProDiMo, fname: str = "C13O_C12O_ratio.out"):
    """
    Reads the file ``C13O_C12O_ratio.out``, if it exists, and fills
    :attr:`~prodimo.read.Data_ProDiMo.isoratio_12CO13CO
    """
    if not os.path.exists(os.path.join(pdata.directory, fname)):
        return

    f, dummy = _getfile(fname, pdata.directory, suppressMsg=False)
    if f is None:
        return None

    ratio = np.loadtxt(f, skiprows=1, usecols=(2))
    pdata.isoratio_12CO13CO = np.flip(np.reshape(ratio, (pdata.nx, pdata.nz), order="F"), axis=1)
    f.close()
    return


def _read_lineEstimateRinfo(pdata, lineEstimate):
    """
    Reads the additional Rinfo data for the given lineEstimate.
    """
    f, dummy = _getfile(pdata.__fpFlineEstimates, None, binary=True, suppressMsg=True)
    if f is None:
        return None

    f.seek(lineEstimate.__posrInfo, 0)
    nxrange = list(range(pdata.nx))
    lineEstimate.rInfo = list()
    for j in nxrange:
        fieldsR = f.readline().decode().split()
        ix = int(fieldsR[0].strip())
        iz = int(fieldsR[1].strip())
        Fcolumn = float(fieldsR[2])
        tauLine = _convToFloatCheck(fieldsR[3], ix, iz, "tauLine")
        tauDust = _convToFloatCheck(fieldsR[4], ix, iz, "tauDust")
        z15 = (float(fieldsR[5]) * u.cm).to(u.au).value
        z85 = (float(fieldsR[6]) * u.cm).to(u.au).value
        ztauD1 = None
        Ncol = None
        if pdata.__versionFlineEstimates == 3:
            ztauD1 = _convToFloatCheck(fieldsR[7], ix, iz, "ztauD1")
            Ncol = float(fieldsR[8])

        # ix -1 and iz-1 because in python we start at 0

        rInfo = DataLineEstimateRInfo(
            ix - 1, iz - 1, Fcolumn, tauLine, tauDust, z15, z85, ztauD1, Ncol
        )
        lineEstimate.rInfo.append(rInfo)

    f.close()


def read_linefluxes(directory, filename="line_flux.out"):
    """Reads the line fluxes output. Can deal with multiple inclinations.

    Parameters
    ----------
    directory : str
      the model directory.

    filename : str
      the filename of the output file (optional).

    Returns
    -------
    list(:class:`prodimopy.read.DataLine`)
      List of lines.
    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    records = f.readlines()
    f.close()

    dist = float(records[0].split("=")[1])  # type: ignore
    nlines = int(records[2].split("=")[1])  # type: ignore
    nvelo = int(records[3].split("=")[1])  # type: ignore

    lines = list()

    # determine if there are multiple inclinations
    # likely very slow
    ninc = sum("inclination[degree]" in s for s in records)  # type: ignore
    # this might be faster, but also a bit dirtz
    # nrecords=len(records)
    # nlinesinc=4+nlines*(5+nvelo)+2
    # print(nrecords,nlinesinc,(nrecords+2)/nlinesinc)

    pos = 5

    # loop for all inclinations
    for iinc in range(ninc):
        # print("start",iinc,pos,records[pos])
        incl = float(records[pos - 4].split("=")[1])  # type: ignore
        # print(incl)
        # print()
        # loop over all lines
        for i in range(nlines):
            # read the data for one line this the same data for inclinations

            if iinc == 0:
                line = DataLine()
                rec = records[pos]
                # try a new method that should work for all versions of line_flux output
                # deals now also with eh _lte stuff (although hardcoded)
                try:
                    fields = rec.split()
                    line.ident = fields[1].strip()
                    # extract the species
                    # TODO: nothing done for e.g. OI OII etc. could also be OI_LTE
                    if line.ident.endswith(("_lte", "_LTE")):
                        line.species = line.ident[:-4]
                    # Hitran molecules (check for isotopologues)
                    elif line.ident.endswith(("_H")):
                        line.species = line.ident[:-2]
                    else:
                        line.species = line.ident

                    line.prodimoInf = fields[2].strip() + fields[3].strip()  # type: ignore
                    line.wl = float(fields[6].strip()[:-3])  # get rid of the mic unit
                    line.frequency = float(fields[9].strip()[:-3])  # get rid of the GHz
                except:  # noqa: E722
                    try:  # FIXME: those could be removed, the general way should work for all of them
                        print("WARN: read_linefluxes: try older format")
                        line.species = (rec[10:20]).strip()
                        line.ident = line.species
                        line.prodimoInf = rec[21:41].strip()
                        line.wl = float(rec[48:64].strip())  # *u.um
                        line.frequency = float(rec[74:90].strip())  # *u.GHz
                    except:  # noqa: E722
                        print("WARN: read_linefluxes: try even older format")
                        line.species = (rec[10:20]).strip()
                        line.ident = line.species
                        line.prodimoInf = rec[21:36].strip()
                        line.wl = float(rec[43:54].strip())  # *u.um
                        line.frequency = float(rec[63:76].strip())  # *u.GHz

                line.distance = dist
            else:
                # get the line that was already initialised
                line = lines[i]

            # thisis data the changes for each inclination
            rec = records[pos + 1]
            line._fluxs.append(float(rec.split("=")[1].strip()))  # type: ignore   *u.Watt/u.m**2

            rec = records[pos + 2]
            line._fconts.append(float(rec.split("=")[1].strip()))  # type: ignore   *u.Jansky

            # simply store inclination and distance for each line

            line._inclinations.append(incl)

            # one line in the profile is for the continuum
            profile = DataLineProfile(nvelo - 1, restfrequency=line.frequency)

            for j in range(nvelo - 1):
                # skip the header line and the first line (continuum)?
                fields = records[pos + 5 + j].split()
                profile.velo[j] = float(fields[0])  # *u.km/u.s
                profile.flux[j] = float(fields[1])  # *u.Jansky
                if len(fields) > 2:
                    profile.flux_conv[j] = float(fields[2])  # *u.Jansky
                if len(fields) > 3:
                    profile.flux_dust[j] = float(fields[3])  # *u.Jansky
            line._profiles.append(profile)

            # don't add the object again
            if iinc == 0:
                lines.append(line)

            pos += nvelo + 5
        pos += 6

    return lines


def read_lineObs(directory, nlines, filename="LINEobs.dat"):
    """
    Reads the lineobs Data. the number of lines have to be known.
    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    records = f.readlines()
    f.close()

    linesobs = list()
    versionStr = records[0].split()
    version = float(versionStr[0])

    for rec in records[2 : 2 + nlines]:
        fields = rec.split()

        lineobs = DataLineObs(
            float(fields[0].strip()),
            float(fields[1].strip()),
            float(fields[2].strip()),
            float(fields[3].strip()),
            fields[4].strip(),
        )

        # in case of upper limits flux might be zero in that case use sig.
        if lineobs.flux < 1.0e-100:
            lineobs.flux = lineobs.flux_err

        linesobs.append(lineobs)

    # the additional data
    # check if there is actually more data
    if len(records) > 2 + nlines + 1:
        # FIXME: do this proberly (the reading etc. and different versions)
        profile = (records[2 + nlines + 1].split())[0:nlines]
        # autoC = (records[2 + nlines + 2].split())[0:nlines]
        # vvalid = (records[2 + nlines + 3].split())[0:nlines]

        # speres = (records[2 + nlines+4].split())[0:nlines]

        offset = 5
        if version > 2.0:
            offset = 6

        # now go through the profiles
        for i in range(nlines):
            proffilename = records[offset + nlines + i + 1].strip()
            if profile[i] == "T":
                if "nodata" == proffilename:
                    print("WARN: Something is wrong with line " + str(i))
                linesobs[i].profile, linesobs[i].profileErr = read_lineObsProfile(
                    proffilename, directory=directory
                )

    return linesobs


def read_lineObsProfile(filename, directory="."):
    """
    reads a line profile file which can be used for |prodimo|
    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    records = f.readlines()
    f.close()

    # First line number of velo points and central wavelength, which we do not
    # need here (I think this is anyway optional
    nvelo = int(records[0].split()[0].strip())

    # skip header lines
    profile = DataLineProfile(nvelo)
    for i in range(2, nvelo + 2):
        fields = records[i].split()
        profile.velo[i - 2] = float(fields[0].strip())
        profile.flux[i - 2] = float(fields[1].strip())
        # also fill the convolved flux, which is just the same as the flux
        # for observations
        profile.flux_conv[i - 2] = profile.flux[i - 2]

    # Check if there is actually an error field.
    if (nvelo + 2) >= len(records):
        err = 0.0
    else:
        if records[nvelo + 2].strip() != "":
            err = float(records[nvelo + 2].split()[0].strip())
        else:
            err = 0.0

    return profile, err


def read_gas(directory, filename="gas_cs.out"):
    """
    Reads gas_cs.out

    Returns
    -------
    :class:`~prodimopy.read.DataGas`

    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    nlam = int(f.readline().strip())

    # skip one line
    f.readline()

    gas = DataGas(nlam)

    for i in range(nlam):
        fields = [float(field) for field in f.readline().split()]
        gas.lam[i] = float(fields[0])
        gas.abs_cs[i] = float(fields[1])
        gas.sca_cs[i] = float(fields[2])

    gas.energy[:] = ((gas.lam[:] * u.micron).to(u.eV, equivalencies=u.spectral())).value

    f.close()

    return gas


def read_continuumImages(directory, filename="image.out"):
    """
    Reads the image.out file.

    To avoid unnecessary memory usage, the Intensities are not read in this
    routine. For this use :func:`~prodimopy.read.DataContinuumImages.get_image`
    """

    f, fname = _getfile(filename, directory=directory)

    if f is None:
        return None

    incl = float(f.readline().split()[0])
    nrnt = f.readline().split()
    nlam = f.readline().split()[0]

    # FIXME: passing incl ist not useful in case of multiple inclinations
    images = DataContinuumImages(int(nlam), int(nrnt[0]), int(nrnt[1]), incl=incl, filepath=fname)

    images.lams[:] = np.array(f.readline().split()).astype(float)
    f.close()

    # Read the coordinates, that is just for the first inclination
    xy = np.loadtxt(fname, skiprows=6, usecols=(2, 3), max_rows=images.nx * images.ny)
    images.x = xy[:, 0].reshape(images.nx, images.ny)
    images.y = xy[:, 1].reshape(images.nx, images.ny)

    return images


def read_continuumObs(directory, filename="SEDobs.dat"):
    """
    Read observational continuum data (SED).

    Looks for and reads the following files:
      - ``SEDobs.dat`` photometric data points.
      - ``PREFIXspec.dat`` where prefix can be `Spitzer, ISO, PACS, SPIRE, JWST`
      - ``extinct.dat`` extinction data used to redden the simulated SED.

    All files are optional. The information is then used to e.g. overplot the observational data
    in :func:`~prodimopy.plot.Plot.plot_sed`).
    """
    contObs = None
    rfile = directory + "/" + filename
    if os.path.exists(rfile):
        print("READ: Reading File: ", rfile, " ...")
        f = open(rfile, "r")

        nlam = int(f.readline().strip())
        f.readline()  # header line
        contObs = DataContinuumObs(nlam=nlam)
        for i in range(nlam):
            elems = f.readline().split()
            contObs.lam[i] = float(elems[0])
            contObs.fnuJy[i] = float(elems[1])
            contObs.fnuJyErr[i] = float(elems[2])
            contObs.flag[i] = str(elems[3])

        contObs.nu = (contObs.lam * u.micrometer).to(u.Hz, equivalencies=u.spectral()).value
        contObs.fnuErg = (contObs.fnuJy * u.Jy).cgs.value
        contObs.fnuErgErr = (contObs.fnuJyErr * u.Jy).cgs.value
        f.close()

    # check for the spectrum files
    # types of spectra that are understood, is more of a unofficial naming convention
    types = ["Spitzer", "ISO", "PACS", "SPIRE", "JWST"]
    fnames = list()
    for spectype in types:
        fnames.extend(glob.glob(directory + "/" + spectype + "*spec*.dat"))

    if fnames is not None and len(fnames) > 0:
        if contObs is None:
            contObs = DataContinuumObs()
        contObs.specs = list()

    for fname in fnames:
        print("READ: Reading File: ", fname, " ...")
        # use basename in the if to avoid problems with directory names
        # containing the string of one of the types.
        if types[0] in os.path.basename(fname):
            spec = np.loadtxt(fname, skiprows=3)
        elif types[1] in os.path.basename(fname):
            spec = np.loadtxt(fname, skiprows=1)
        elif types[2] in os.path.basename(fname):
            spec = np.loadtxt(fname)
        elif types[3] in os.path.basename(fname):
            spec = np.loadtxt(fname, skiprows=1)
            # convert frequency to micron, SPIRE data
            spec[:, 0] = (spec[:, 0] * u.GHz).to(u.micron, equivalencies=u.spectral()).value
        elif types[4] in os.path.basename(fname):
            spec = np.loadtxt(fname, skiprows=3)
        else:
            print("Don't know about type of " + fname + " Spectrum. Try anyway")
            spec = np.loadtxt(fname)

        # If there is no error provided just add a zero column
        if spec.shape[1] < 3:
            spec = np.c_[spec, np.zeros(spec.shape[0])]

        contObs.specs.append(spec)

    # check if there is some extinction data available
    fn_ext = directory + "/extinct.dat"
    if os.path.exists(fn_ext):
        print("READ: Reading File: ", fn_ext, " ...")
        if contObs is None:
            contObs = DataContinuumObs()

        fext = open(fn_ext, "r")
        fext.readline()
        contObs.E_BV = float(fext.readline())
        fext.readline()
        contObs.R_V = float(fext.readline())
        contObs.A_V = contObs.R_V * contObs.E_BV

        fext.close()

    #   # check if there is an image.in
    #   fn_images= directory+"/image.in"
    #   if os.path.exists(fn_images):
    #     if contObs is None:
    #       contObs=DataContinuumObs()
    #
    #     fext= open(fn_images,"r")
    #     fext.readline()
    #     fext.readline()
    #     nimages=int(fext.readline())
    #     positionAngle = float(fext.readline())
    #
    #     for i in range(9):
    #       line = f.readline()

    return contObs


def read_FLiTs(directory, filename="specFLiTs.out"):
    """
    Reads the FLiTs spectrum.

    Returns
    -------
    :class:`prodimopy.read.DataFLiTsSpec`
      The Spectrum.

    """
    f, pfilename = _getfile(filename, directory)
    if f is None:
        return None, None
    f.close()

    # currently read only the wavelength and the total flux and the continuum (col 3)
    # doesn't work for including the continuum
    #
    # likely slow, just to get the number of entries

    f = open(pfilename)
    lines = f.readlines()

    nent = len(lines)
    specFLiTs = DataFLiTsSpec()
    specFLiTs.wl = np.zeros(shape=(nent))
    specFLiTs.flux = np.zeros(shape=(nent))
    specFLiTs.flux_cont = np.zeros(shape=(nent))

    for i, line in enumerate(lines):
        arr = line.split()
        # sometimes only the first two columns a filled, deal with it
        specFLiTs.wl[i] = float(arr[0])
        specFLiTs.flux[i] = float(arr[1])

        # fill the continuum just from the first column as it is sometime empty
        # FIXME: not sure while sometimes FLiTs does not produce a continuum value, this is just a workaround
        if len(arr) == 2:
            specFLiTs.flux_cont[i] = float(arr[1])
        else:
            specFLiTs.flux_cont[i] = float(arr[3])

    f.close()

    return specFLiTs


def read_sed(directory, filename="SED.out", filenameAna="SEDana.out"):
    """
    Reads the |prodimo| SED output including the analysis data.
    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    records = f.readlines()
    f.close()

    # determine if there are multiple inclinations
    # likely very slow
    # -1 becaus we ignore the analytic one
    ninc = sum("inclination[degree]" in s for s in records) - 1

    distance = float(records[0].split()[-1])
    nlam = int(records[2])

    sed = DataSED(nlam, distance)

    ridx = nlam + 2 + 3

    # need this already here
    sed._Lbols = [None] * ninc
    sed._Tbols = [None] * ninc

    for iinc in range(ninc):
        sed._inclinations.append(float(records[ridx].split()[-1]))
        ridx += 3

        fnuErg = np.zeros(shape=(nlam))
        nuFnuW = np.zeros(shape=(nlam))
        fnuJy = np.zeros(shape=(nlam))

        for i in range(nlam):
            elems = records[ridx].split()
            if iinc == 0:
                sed.lam[i] = float(elems[0])
                sed.nu[i] = float(elems[1])

            # FIXME: Workaround to catch strange values from ProDiMo .. should be fixed
            # in ProDiMo
            try:
                fnuErg[i] = float(elems[2])
                nuFnuW[i] = float(elems[3])
                fnuJy[i] = float(elems[4])
            except ValueError as err:
                print("WARN: Could not read value from SED.out: ", err)
            ridx += 1

        sed._fnuErgs.append(fnuErg)
        sed._nuFnuWs.append(nuFnuW)
        sed._fnuJys.append(fnuJy)

        sed._incidx = iinc
        sed.setLbolTbol()
        # next inc
        ridx += 1

    sed._incidx = 0  # reset to the first inclination

    # The analysis data, if it is not there not a big problem
    f, dummy = _getfile(filenameAna, directory)
    if f is None:
        sed.sedAna = None
        return sed

    nlam, nx = f.readline().split()
    nlam = int(nlam)
    nx = int(nx)

    sed.sedAna = DataSEDAna(nlam, nx)

    for i in range(nlam):
        elems = f.readline().split()
        sed.sedAna.lams[i] = float(elems[0])
        sed.sedAna.r15[i] = float(elems[1])
        sed.sedAna.r85[i] = float(elems[2])
        for j in range(nx):
            elems = f.readline().split()
            sed.sedAna.z15[i, j] = float(elems[0])
            sed.sedAna.z85[i, j] = float(elems[1])

    f.close()

    return sed

def read_star(directory: str, filenameSpec: str ="StarSpectrum.out", filenameRTinterpol: str ="RTinterpolation.out"):
    """
    Reads `StarSpectrum.out` and `RTinterpolation.out` if it exists.

    Calls :func:`~prodimopy.read.read_starSpec` for the `StarSpectrum.out`

    Parameters
    ----------

    directory : 
        The model directory.

    filenameSpec : 
        The filename for the star spectrum. Default: "StarSpectrum.out"

    filenameRTinterpol : 
        The filename for the RT interpolation data. Default: "RTinterpolation.out"
    """

    # Also creates the star object
    # FIXME: is not so nice, but comes from old implementation for starSpec
    star=read_starSpec(directory,filename=filenameSpec)

    f, dummy = _getfile(filenameRTinterpol, directory,suppressMsg=True)
    if f is None:
        return star

    lines= f.readlines()    
    nbands=int(lines[1])
    star._lambs=np.array([float(line.split()[0]) for line in lines[2:2+nbands+1]])
    star.InuBand=np.array([float(line.split()[2]) for line in lines[2+nbands+1:2+2*nbands+1]])

    # can be different to Starlam actually
    star.wlInterpol=np.array([float(line.split()[0]) for line in lines[2+2*nbands+1+1:]])    
    star.InuInterpol=np.array([float(line.split()[2]) for line in lines[2+2*nbands+1+1:]])
            
    f.close()

    return star


def read_starSpec(directory: str, filename: str ="StarSpectrum.out"):
    """
    Reads StarSpectrum.out

    Parameters
    ----------

    directory :
        The model directory.

    filename :
        The filename. Default: "StarSpectrum.out"

    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    teff = float((f.readline().split())[-1])
    elems = f.readline().split()
    r = float(elems[-1])
    logg = float(elems[2])
    luv = float(f.readline().split()[-1])
    nlam = int(f.readline())
    f.readline()

    starSpec = DataStar(nlam, teff, r, logg, luv)
    for i in range(nlam):
        elems = f.readline().split()
        starSpec.lam[i] = float(elems[0])
        starSpec.nu[i] = float(elems[1])
        starSpec.Inu[i] = float(elems[2])

    f.close()
    return starSpec


def read_bgSpec(directory, filename="BgSpectrum.out"):
    """
    Reads the BgSpectrum.out file.

    Returns
    -------
      :class:`prodimopy.read.DataBgSpec`
      the background spectra or `None` if not found.
    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    nlam = int(f.readline())
    f.readline()

    bgSpec = DataBgSpec(nlam)
    for i in range(nlam):
        elems = f.readline().split()
        bgSpec.lam[i] = float(elems[0])
        bgSpec.nu[i] = float(elems[1])
        bgSpec.Inu[i] = float(elems[2])

    return bgSpec


def read_dust(directory, filename="dust_opac.out"):
    """
    Reads `dust_opac.out` and if it exists `dust_sigmaa.out`.
    Does not read the dust composition yet.

    Returns
    -------
    :class:`~prodimopy.read.DataDust`

    """
    f, dummy = _getfile(filename, directory)
    if f is None:
        return None

    fields = [int(field) for field in f.readline().split()]
    ndsp = fields[0]
    nlam = fields[1]

    # skip three lines
    for i in range(ndsp):
        f.readline()

    # apow amax etc.
    strings = f.readline().split()

    if len(strings) > 0:
        amin = ((float(strings[6]) * u.cm).to(u.micron)).value
        amax = ((float(strings[7]) * u.cm).to(u.micron)).value
        apow = float(strings[8])
        nsize = int(strings[9])
        dust = DataDust(amin, amax, apow, nsize, nlam)
    else:
        dust = DataDust(-1, -1, 0.0, -1, nlam)

    f.readline()

    for i in range(nlam):
        fields = [float(field) for field in f.readline().split()]
        dust.lam[i] = float(fields[0])
        dust.kext[i] = float(fields[1])
        dust.kabs[i] = float(fields[2])
        dust.ksca[i] = float(fields[3])

        if len(fields) > 4:
            dust.ksca_an[i] = float(fields[5])  # skip kprn

    f.close()

    dust.energy[:] = ((dust.lam[:] * u.micron).to(u.eV, equivalencies=u.spectral())).value

    # is optional but returns None if file is not there
    # does not have to be there
    dust.asize, dust.sigmaa = read_dust_sigmaa(directory)

    return dust


def read_dust_sigmaa(directory, filename="dust_sigmaa.out"):
    """
    Reads the radial surface density profiles for each grain size.

    Parameters
    ----------

    directory : str
      The directory where the file is located (the |prodimo| model directory).

    filename : str
      The filename. Default: "dust_sigmaa.out"

    """

    if not os.path.isfile(os.path.join(directory, filename)):
        return None, None

    f, pfilename = _getfile(filename, directory)
    if f is None:
        return None, None
    f.close()  # don't  need it use np for simplicity

    # a bit quick an dirty
    data = np.loadtxt(pfilename, comments="#")

    # the first row in the array are the grain sizes.
    # convert from cm to micron
    asize = (data[0, :] * u.cm).to(u.micron).value
    # used transposed array, to be consistent with ohter stuff.
    sigmaa = np.transpose(data[1:, :])

    return asize, sigmaa


def calc_NHrad_oi(data):
    """
    Calculates the radial column density from out to in (border of model space to star/center)

    .. todo::

        - is this really needed, should rather be a method within :class:`prodimopy.read.Data_ProDiMo`
    """

    NHradoi = 0.0 * data.nHtot
    for ix in range(data.nx - 2, 1, -1):  # first ix point (ix=0= remains zero
        r1 = (data.x[ix + 1, :] ** 2 + data.z[ix + 1, :] ** 2) ** 0.5
        r2 = (data.x[ix, :] ** 2 + data.z[ix, :] ** 2) ** 0.5
        dr = r1 - r2
        dr = dr * u.au.to(u.cm)
        nn = 0.5 * (data.nHtot[ix + 1, :] + data.nHtot[ix, :])
        NHradoi[ix, :] = NHradoi[ix + 1, :] + nn * dr

    return NHradoi


def calc_surfd(data):
    """
    Caluclates the gas and dust vertical surface densities at every point in the
    model.

    Only one half of the disk is considered. If one needs the total surface density
    simply multiply the value from the midplane (zidx=0) by two.

    """
    print("INFO: Calculate surface densities")

    tocm = (1.0 * u.au).to(u.cm).value
    data._sdg = 0.0 * data.rhog
    data._sdd = 0.0 * data.rhod
    for ix in range(data.nx):
        for iz in range(data.nz - 2, -1, -1):  # from top to bottom
            dz = data.z[ix, iz + 1] - data.z[ix, iz]
            dz = dz * tocm
            nn = 0.5 * (data.rhog[ix, iz + 1] + data.rhog[ix, iz])
            data._sdg[ix, iz] = (
                data._sdg[
                    ix,
                    iz + 1,
                ]
                + nn * dz
            )
            nn = 0.5 * (data.rhod[ix, iz + 1] + data.rhod[ix, iz])
            data._sdd[ix, iz] = (
                data._sdd[
                    ix,
                    iz + 1,
                ]
                + nn * dz
            )


def _calc_vol(data):
    """
    Inits the vol field (:attr:`~prodimpy.read.Data_ProDiMo._vol` for each individual grid point.

    This is useful to estimate mean quantities which are weighted by volume
    but also by mass.

    The routine follows the same method as in the prodimo.pro (the IDL skript)

    """

    print("INFO: Calculate volumes")
    tocm = (1.0 * u.au).to(u.cm).value
    data._vol = np.zeros(shape=(data.nx, data.nz))
    fourthreepi = 4.0 * math.pi / 3.0
    for ix in range(data.nx):
        ix1 = np.max([0, ix - 1])
        ix2 = ix
        ix3 = np.min([data.nx - 1, ix + 1])
        x1 = math.sqrt(data.x[ix1, 0] * data.x[ix2, 0]) * tocm
        x2 = math.sqrt(data.x[ix2, 0] * data.x[ix3, 0]) * tocm  # does not depend on iz
        for iz in range(data.nz):
            iz1 = np.max([0, iz - 1])
            iz2 = iz
            iz3 = np.min([data.nz - 1, iz + 1])
            tanbeta1 = 0.5 * (data.z[ix, iz1] + data.z[ix, iz2]) / data.x[ix, 0]
            tanbeta2 = 0.5 * (data.z[ix, iz2] + data.z[ix, iz3]) / data.x[ix, 0]
            data.vol[ix, iz] = fourthreepi * (x2**3 - x1**3) * (tanbeta2 - tanbeta1)

    # Test for volume stuff ... total integrated mass
    # mass=np.sum(np.multiply(data.vol,data.rhog))
    # print("Total gas mass",(mass*u.g).to(u.M_sun))


def _calc_cdnmol(data):
    """
    Calculated the vertical column number densities for every species
    at every point in the disk (from top to bottom). Very simple and rough method.

    Only one half of the disk is considered. If one needs the total surface density
    simply multiply the value from the midplane (zidx=0) by two.

    """

    if data._log:
        print("INFO: Calculate vertical column densities")

    tocm = data._pAUtocm
    data._cdnmol = 0.0 * data.nmol
    for ix in range(data.nx):
        for iz in range(data.nz - 2, -1, -1):  # from top to bottom
            dz = data.z[ix, iz + 1] - data.z[ix, iz]
            dz = dz * tocm
            nn = 0.5 * (data.nmol[ix, iz + 1, :] + data.nmol[ix, iz, :])
            data._cdnmol[ix, iz, :] = data._cdnmol[ix, iz + 1, :] + nn * dz


def _calc_rcdnmol(data):
    """
    Calculated the radial column number densities for every species
    at every point in the disk. Very simple and rough method.

    FIXME: this can be quite inaccurate as the x info for the innermost points is not printed accurately to PRoDiMo.out which cause dr to be zero
    """

    if data._log:
        print("INFO: Calculate radial column densities")

    tocm = (1.0 * u.au).to(u.cm).value
    data._rcdnmol = 0.0 * data.nmol
    for iz in range(data.nz):
        for ix in range(1, data.nx, 1):  # first ix point (ix=0= remains zero
            r1 = (data.x[ix, iz] ** 2 + data.z[ix, iz] ** 2) ** 0.5
            r2 = (data.x[ix - 1, iz] ** 2 + data.z[ix - 1, iz] ** 2) ** 0.5
            dr = r1 - r2
            dr = dr * tocm
            nn = 0.5 * (data.nmol[ix, iz, :] + data.nmol[ix - 1, iz, :])
            data._rcdnmol[ix, iz, :] = data._rcdnmol[ix - 1, iz, :] + nn * dr
    # FIXME: test the integration error can be at most 16% ... good enough for now (most fields are better)
    # nHverC=data._rcdnmol[:,:,data.spnames["H"]]+data._rcdnmol[:,:,data.spnames["H+"]]+data._rcdnmol[:,:,data.spnames["H2"]]*2.0
    # izt=data.nz-2
    # print(nHverC[:,izt],data.NHrad[:,izt])
    # print(np.max(np.abs(1.0-nHverC[1:,:]/data.NHrad[1:,:])))


def _flux_Wm2toJykms(flux, frequency):
    """
    Converts a flux from W m^-2 to Jy km/s

    Parameters
    ----------
    flux: float
      the flux in units of [W m^-2]

    frequency: float
      the frequency of the flux in [GHz]

    Returns
    -------
    float
      The flux of the line. `UNIT: Jansky km s^-1`
    """
    res = flux * u.Watt / (u.m**2.0)
    ckm = const.c.to("km/s")

    res = (res).to(u.Jansky, equivalencies=u.spectral_density(frequency * u.GHz))

    return (res * ckm).value


def _getfile(filename, directory=None, binary=False, suppressMsg=False):
    """
    Utility function to open a particular file from a |prodimo| model.
    """
    pfilename = filename

    if directory is not None:
        pfilename = os.path.join(directory, filename)

    try:
        if binary:
            f = open(pfilename, "rb")
        else:
            f = open(pfilename, "r")
    except:  # noqa: E722
        f = None

    if f is None:
        print(("WARN: Could not open " + pfilename + "!"))
    else:
        if not suppressMsg:
            print(f"READ: {filename} ...")
    return f, pfilename


@deprecated("Use the function prodimopy.read.Data_ProDiMo.analyse_chemistry instead.")
def analyse_chemistry(
    species: str,
    model: Data_ProDiMo,
    to_txt=True,
    td_fileIdx: str | int = None,
    filenameChemistry="chemanalysis.out",
    screenout=True,
) -> Chemistry:
    """

    .. deprecated:: 2.5
      Use :func:`prodimopy.read.Data_ProDiMo.analyse_chemistry` instead.

    Function that analyses the chemistry in a similar way to chemanalysis.pro.

    Parameters
    ----------

    species : str
      The species name one wants to analyze.

    model : :class:`~prodimopy.read.Data_ProDiMo`
      the |prodimo| model data.

    to_txt : boolean
      Write info about formation and destruction reactions for the selecte molecule
      to a txt file. Default: `True`

    td_fileIdx : str or int
      For time-dependent chemanalysis. Provide here the idx for the timestep.
      E.g. `"0001"` for the first one.

    filenameChemistry : str
      The name of the file that holds the reaction rates. Default: `chemanalysis.out`.
      Just in case it has a different name, usually one does not need to change that.

    screenout : boolean
      If `True` all the form./dest. reactions are  printed on the screen. Default: `True`

    Returns
    -------
    :class:`prodimopy.read.Chemistry`
      Object that holds all the required information and can be use for the plotting routines,
      and to analyse the chemistry point by point `func:~pread.Chemistry.reac_rates_ix_iz`.

    """
    import astropy.io.fits as fits

    chemistry = Chemistry(model.name)

    start = timer()

    # stores all the formation reaction indices and rates for each grid point
    gridf = np.empty((model.nx, model.nz, 2), dtype=np.ndarray)
    gridd = np.empty((model.nx, model.nz, 2), dtype=np.ndarray)
    totfrate = np.zeros((model.nx, model.nz))  # total formation rate at each point)
    totdrate = np.zeros((model.nx, model.nz))  # total formation rate at each point)
    fidx = list()  # indices of all unique formation reactions
    didx = list()  # indices of all unique destruction reactions

    # check if already a fits file with the given.out name exits
    fnamefits = filenameChemistry.replace(".out", ".fits")
    if td_fileIdx is not None:
        ext = _td_fileIdx_ext(td_fileIdx)
        fnamefits = fnamefits.replace(".fits", ext + ".fits")

    if os.path.isfile(os.path.join(model.directory, fnamefits)):
        # if so, use it
        print("INFO: Using existing fits file for chemanalysis: ", fnamefits)
        filenameChemistry = fnamefits
    else:
        print("INFO: convert existing txt format file to fits (that can take a bit) ... ")
        # create an array that holds the reaction rates
        rates = np.zeros(
            shape=(model.nx, model.nz, len(model.chemnet.reactions)), dtype=np.float32
        )
        if td_fileIdx is not None:
            # if it is a time-dependent model, the filenameChemistry is different
            # not nice, but ext should be set already
            filenameChemistry = filenameChemistry.replace(".out", ext + ".out")
        fc = open(os.path.join(model.directory, filenameChemistry), "r")

        fc.readline()  # skip the first line
        for line in fc:
            ix, iz, dummy, ireac, rate = line.split()
            rates[int(ix) - 1, int(iz) - 1, int(ireac) - 1] = float(rate)

        fc.close()
        hdu = fits.PrimaryHDU(
            data=rates.T
        )  # transpose to have it in the same order as it would be from prodimo
        hdu.writeto(os.path.join(model.directory, fnamefits), overwrite=True)
        filenameChemistry = fnamefits

    # that gives me simply all formation and desctruction reactions for the given species

    # those include the real ids (e.g. starts at 1) and not the zero-based python indices!!
    fidx = np.array([x.id for x in model.chemnet.reactions if species in x.products])
    didx = np.array([x.id for x in model.chemnet.reactions if species in x.reactants])

    # now read all info from the fits file
    cfits = fits.open(
        os.path.join(model.directory, filenameChemistry), do_not_scale_image_data=True, memmap=True
    )
    formrates = cfits[0].data[fidx - 1, :, :]  # is read in reversed order for the dims
    destrates = cfits[0].data[didx - 1, :, :]
    formrates = formrates.T  # transpose it to have it in nx,nz,ncreac ...
    destrates = destrates.T  # transpose it to have it in nx,nz,ncreac ...
    cfits.close()

    # sorted indices for the formation and destruction rates
    formridx = np.flip(np.argsort(formrates, axis=2), axis=2)  # reversed order
    destridx = np.flip(np.argsort(destrates, axis=2), axis=2)  # reversed order

    for ix in range(model.nx):
        for iz in range(model.nz):
            gridf[ix, iz, 0] = fidx[formridx[ix, iz, :]]  # formation reaction indices, sorted
            gridf[ix, iz, 1] = formrates[ix, iz, formridx[ix, iz, :]]
            gridd[ix, iz, 0] = didx[destridx[ix, iz, :]]  # destruction reaction indices, sorted
            gridd[ix, iz, 1] = destrates[ix, iz, destridx[ix, iz, :]]

    totfrate[:, :] = np.sum(formrates, axis=2)  # total formation rate at each point
    totdrate[:, :] = np.sum(destrates, axis=2)  # total destruction rate at each point

    chemistry.species = species
    chemistry.gridf = gridf
    chemistry.gridd = gridd
    chemistry.fridxs = fidx
    chemistry.dridxs = didx
    chemistry.totfrate = totfrate
    chemistry.totdrate = totdrate
    # reference to the model
    chemistry.model = model

    if to_txt:
        output_chem_fname = os.path.join(
            model.directory, "chemistry_reactions_" + species + ".txt"
        )
        if td_fileIdx is not None:
            output_chem_fname = output_chem_fname.replace(".txt", ext + ".txt")
        f = open(output_chem_fname, "w")
        f.writelines("-------------------------------------------------------\n")
        f.writelines("formation and destruction reactions \n")
        f.writelines("species: " + species + "\n\n")
        f.writelines("Formation reactions\n")
        for i, ridx in enumerate(chemistry.fridxs):
            f.writelines(chemistry.reac_to_str(model.chemnet.reactions[ridx - 1], i + 1))
            f.writelines("\n")
        f.writelines("\n\n")
        f.writelines("Destruction reactions\n")
        for i, ridx in enumerate(chemistry.dridxs):
            f.writelines(chemistry.reac_to_str(model.chemnet.reactions[ridx - 1], i + 1))
            f.writelines("\n")
        f.writelines("-------------------------------------------------------\n")
        f.close()
        print("Writing information to: " + output_chem_fname)

        # also print it to stdout
        if screenout:
            with open(output_chem_fname) as f:
                print(f.read())

    print("INFO: Calc time: ", "{:4.2f}".format(timer() - start) + " s")
    return chemistry


@deprecated("Use the function prodimopy.read.Chemistry.reac_rates_ix_iz instead.")
def reac_rates_ix_iz(model, chemana, ix=None, iz=None, locau=None, lowRatesFrac=1.0e-3):
    """

    .. deprecated:: 2.5
      Use :func:`prodimopy.read.Chemistry.reac_rates_ix_iz` instead.

    Function that analyses the chemana manually via a point-by-point
    analysis for a given species. Shows the most important formation and destruction rates for the given point ix,iz (or in au via Parameter `locau`).

    Parameters
    ----------

    model : :class:`~prodimopy.read.Data_ProDiMo`
      the model data

    chemana : :class:`~prodimopy.read.Chemistry`
      data resulting from :func:`~prodimopy.read.analyse_chemistry` on a single species

    ix : int
      ix corresponding to desired radial location in grid, starting at 0

    iz : int
      iz corresponding to desired radial location in grid, starting at 0

    locau : array_like
      the desired coordinates in au [x,z]. The routine then finds the closest
      grid point for those coordinates.

    lowRatesFrac : float
      Only rates with rate/total_rate > lowRatesFrac are printed. Default: 1.e-3
      This is useful to avoid printing all the reactions that are not important.
    """

    if locau is not None:
        ix = np.argmin(np.abs(model.x[:, 0] - locau[0]))
        iz = np.argmin(np.abs(model.z[ix, :] - locau[1]))

    if ix is None or iz is None:
        print("Please provide either ix,iz or locau!")
        return

    print("Analysing point x=", str(model.x[ix, iz]) + " au z=" + str(model.z[ix, iz]) + " au")

    print("      Detailed reaction rates for: %10s" % chemana.species)
    print(
        "------------------------------------------------------------------------------------------------------"
    )

    print("                    grid point = %i       %i" % (ix, iz))
    print("        r,z [au] (cylindrical) = %.3f  %.4f" % (model.x[ix, iz], model.z[ix, iz]))
    print("               n<H>,nd [cm^-3] = %.1e  %.1e" % (model.nHtot[ix, iz], model.nd[ix, iz]))
    print("                Tgas,Tdust [K] = %.1e  %.1e" % (model.tg[ix, iz], model.td[ix, iz]))
    print(
        "                 AV_rad,AV_ver = %.1e  %.1e" % (model.AVrad[ix, iz], model.AVver[ix, iz])
    )
    print(
        "          %10s" % chemana.species
        + " abundance = %e" % model.getAbun(chemana.species)[ix, iz]
    )
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    print(" Total form. rate [cm^-3 s^-1] = {:10.2e}".format(chemana.totfrate[ix, iz]))
    for i, ridx in enumerate(chemana.gridf[ix, iz, 0]):
        rate = chemana.gridf[ix, iz, 1][i]
        if rate / chemana.totfrate[ix, iz] > lowRatesFrac:  # don't print low rates
            print(
                chemana.reac_to_str(
                    model.chemnet.reactions[ridx - 1],
                    list(chemana.fridxs).index(ridx) + 1,
                    rate=rate,
                )
            )
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    print(" Total dest. rate [cm^-3 s^-1] = {:10.2e}".format(chemana.totdrate[ix, iz]))
    for i, ridx in enumerate(chemana.gridd[ix, iz, 0]):
        rate = chemana.gridd[ix, iz, 1][i]
        if rate / chemana.totdrate[ix, iz] > lowRatesFrac:  # don't print unimportant rates
            print(
                chemana.reac_to_str(
                    model.chemnet.reactions[ridx - 1],
                    list(chemana.dridxs).index(ridx) + 1,
                    rate=rate,
                )
            )
    print(
        "------------------------------------------------------------------------------------------------------"
    )
    print("")
