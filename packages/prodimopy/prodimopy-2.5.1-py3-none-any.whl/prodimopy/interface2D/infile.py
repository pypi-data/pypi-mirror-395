"""
Tools to generated input files for the |prodimo| 2D interface.
"""

import os
from copy import deepcopy

import numpy as np
from prodimopy.read import Data_ProDiMo

# FIXME: not nice, but use the au to cm conversion constant from ProDiMo
# just to be consistent
autocm = 1.495978700e13


class Interface2Din(object):
    """
    Some utility class to generate input files for the |prodimo| 2D interface.

    .. todo:

      - it might makes sense to actually use the :class:`~prodimopy.read.Data_ProDiMo`
        class to fill the values from the 2D input structure (e.g. from a hydro model).
        That would then also to directly plot the input. One could get rid
        of the :func:`get_pmodel` method.
    """

    def __init__(
        self, x, z, rhoGas=None, nHtot=None, velocity=None, g2d=None, tdust=None, tgas=None
    ):
        """

        Parameters
        ----------

        x : array_like(dim=(nx,nz))
          the x (radial coordinates) in cm

        z : array_like(dim=(nx,nz))
          the z (vertical coordinates) in cm

        rhoGas : array_like(dim=(nx,nz))
          gas density in (|gcm^-3|; optional. But either nHtot or rhoGas have to be provided

        nHtot : array_like(dim=(nx,nz))
          hydrogen number density in (|cm^-3|; optional

        velocity : array_like(dim=(nx,nz,3))
          velocity field (vx,vy,vz) in cm/s; optional

        g2d : array_like(dim=(nx,nz))
          gas to dust mass ratio; optional

        tdust : array_like(dim=(nx,nz))
          dust temperature in K; optional

        tgas : array_like(dim=(nx,nz))
          gas temperature in K; optional


        Attributes
        ----------

        """

        if nHtot is None and rhoGas is None:
            raise Exception("Either nHtot or rhoGas have to be specified.")

        self.nx: int = x.shape[0]
        """ : number of x grid points """
        self.nz: int = x.shape[1]
        """ : number of z grid points """
        self.x = x
        """ array_like(dim=(nx,nz)) :
      x coordinates in cm (Cartesian
    """
        self.z = z
        """ array_like(dim=(nx,nz)) :
      z coordinates in cm (Cartesian)
    """
        self.rhoGas = rhoGas
        """ array_like(dim=(nx,nz)) :
      gas density in |gcm^-3|
    """
        self.nHtot = nHtot
        """ array_like(dim=(nx,nz)) :
      total hydrogen number density in |cm^-3|
    """
        self.velocity = velocity
        """ array_like(dim=(nx,nz,3)) :
      velocity vector vx,vy,vz in |cms^-1|
    """
        self.g2d = g2d
        """ array_like(dim=(nx,nz)) :
      gas to dust mass ratio at every point
    """
        self.tdust = tdust
        """ array_like(dim=(nx,nz)) :
      Dust temperature in K. Is not yet written to the |prodimo| input file.
      But can be useful for comparisons
    """
        self.tgas = tgas
        """ array_like(dim=(nx,nz)) :
      Gas temperature in K. Is not yet written to the |prodimo| input file.
      But can be useful for comparisons
    """

    def interpol_spherical(
        self, pmodel: Data_ProDiMo, imethod: str = "linear", fixmethod: int = 1
    ):
        """
        Interpolation onto the |prodimo| assuming the input grid was spherical.
        E.g. the routines tries to deal with the curvatures at the inner and outer edge.

        Parameters
        ----------

        pmodel :
            the prodimopy model onto which the input structure should be interpolated.

        imethod :
            interpolation method passed to `scipy.interpolate.griddata`.

        fixmethod :
            Method to fix some problems in the interpolated grid. Doesn't necessarily work well, so if you don't need it don't use it.

            0 or None: no fixing
            1: fix vertical columns first (density should always increase towards midplane), Default.
            2: similar to 1 but different approach (not sure any more)
            3: fix only the azimuthal velocity vy (should never be negative in the disk region)

        """
        from scipy.interpolate import griddata

        points = np.array([self.x.flatten() / autocm, self.z.flatten() / autocm]).T

        # can only use nearest, because griddata does not extrapolation ... and that causes problems
        # f = interpolate.interp2d(self.x.flatten()/AU, self.z.flatten()/AU, self.nHtot.flatten(), kind='linear',copy=False)

        if self.nHtot is not None:
            print("- Interpolate nHtot ...")
            pnHtot = griddata(points, self.nHtot.flatten(), (pmodel.x, pmodel.z), method=imethod)
        else:
            pnHtot = None

        if self.rhoGas is not None:
            print("- Interpolate rhoGas ...")
            prhoGas = griddata(points, self.rhoGas.flatten(), (pmodel.x, pmodel.z), method=imethod)
        else:
            prhoGas = None

        if self.velocity is not None:
            print("- Interpolate velocity ...")
            pvel = np.zeros(shape=(pmodel.nx, pmodel.nz, 3))
            for vi in range(3):
                pvel[:, :, vi] = griddata(
                    points, self.velocity[:, :, vi].flatten(), (pmodel.x, pmodel.z), method=imethod
                )
        else:
            pvel = None

        # TODO: the following quantities are not included in the various fixing algorithms
        if self.g2d is not None:
            print("- Interpolate g2d ...")
            pg2d = griddata(points, self.g2d.flatten(), (pmodel.x, pmodel.z), method=imethod)
        else:
            pg2d = None

        if self.tdust is not None:
            print("- Interpolate tdust ...")
            ptdust = griddata(points, self.tdust.flatten(), (pmodel.x, pmodel.z), method=imethod)
        else:
            ptdust = None

        if self.tgas is not None:
            print("- Interpolate tgas ...")
            ptgas = griddata(points, self.tgas.flatten(), (pmodel.x, pmodel.z), method=imethod)
        else:
            ptgas = None

        # assumes grid is from spherical so height cannot be larger then the radius
        # make some cut-off grid from spherical coordinates so height cannot be larger then the radius

        cutoff = np.max(self.x) / autocm
        # if the prodimo grid is smaller then the input grid, then take the cut-off from the prodimo grid
        cutoff = np.min([pmodel.x[-1, 0], cutoff])
        print("Cutoff radius: ", cutoff)
        # print(pmodel.z)

        pnx = len(pmodel.x[:, 0])
        pnz = len(pmodel.z[0, :])

        # density to check for NaN etc.
        pdens = pnHtot
        if pdens is None:
            pdens = prhoGas

        # Make sure the the midplane is filled
        # Another security check ... seems that in some grids the z=0 coordinate has NHtot= 0 or close to zero
        # check if it all the points are or close to zero in the midplane.
        if np.all(pdens[:, 0] < 1.0e-40) or np.all(np.isnan(pdens[:, 0])):
            print("Fixing midplane ...")
            pdens[:, 0] = pdens[:, 1]
            if pg2d is not None:
                pg2d[:, 0] = pg2d[:, 1]
            if pvel is not None:
                pvel[:, 0, :] = pvel[:, 1, :]
            if ptdust is not None:
                ptdust[:, 0] = ptdust[:, 1]
            if ptgas is not None:
                ptgas[:, 0] = ptgas[:, 1]

        # fix outer vertical column if necessary
        if np.isnan(pdens[pnx - 1, 0]):
            pdens[pnx - 1, :] = pdens[pnx - 2, :]
            if pg2d is not None:
                pg2d[pnx - 1, :] = pg2d[pnx - 2, :]
            if pvel is not None:
                pvel[pnx - 1, :, :] = pvel[pnx - 2, :, :]
            if ptdust is not None:
                ptdust[pnx - 1, :] = ptdust[pnx - 2, :]
            if ptgas is not None:
                ptgas[pnx - 1, :] = ptgas[pnx - 2, :]

        # get rid of values outside the computational domain
        cutmask = pmodel.z > (cutoff * 1.1)
        pdens[cutmask] = 0.0
        if pvel is not None:
            for vi in range(3):
                pvel[cutmask, vi] = 0.0

        for arr in [pdens, pvel, ptdust, ptgas]:
            if arr is None:
                continue

            cnan = np.isnan(arr)
            if cnan.any():
                print("Found NaNs set them to zero.")
                arr[cnan] = 0.0

        # special treatment for g2d if it is nan set it to a large number
        if pg2d is not None:
            cnan = np.isnan(pg2d)
            if cnan.any():
                print("Found NaNs in g2d set them to 1.e10.")
                pg2d[cnan] = 1.0e10

        # TODO: check this again, doesn't seem to work very good
        if fixmethod == 1:
            # FIXME: I think all this is really not very general
            # fix some stuff in the inner region ... because of the spherical grid of MOCASSIN/PLUTO
            # this assumes that the density always increases towards the midplane (should be the case for disks)
            for ix in range(pnx):
                # print(ix)
                izmax = np.min(
                    (pnz - 2, np.argmin(np.abs(pmodel.z[ix, :] / pmodel.x[ix, :] - 0.5)))
                )
                # print("izmax: ",izmax)
                for iz in range(izmax, -1, -1):  # from top to bottom
                    # print(ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz],pdens[ix,iz])
                    if pdens[ix, iz] < pdens[ix, iz + 1]:
                        print(
                            "Fix (1): ",
                            ix,
                            iz,
                            pmodel.x[ix, iz],
                            pmodel.z[ix, iz],
                            "{:15.5e}".format(pdens[ix, iz]),
                            "{:15.5e}".format(pdens[ix, iz + 1]),
                        )

                        pdens[ix, iz] = pdens[ix, iz + 1]
                        if pg2d is not None:
                            pg2d[ix, iz] = pg2d[ix, iz + 1]

                        if pvel is not None:
                            pvel[ix, iz, 0] = pvel[ix, iz + 1, 0]
                            # pvel[ix,iz,1]=pvel[ix,iz+1,1]
                            pvel[ix, iz, 2] = pvel[ix, iz + 1, 2]

                    # check explicitly for vy
                    if (pvel is not None) and pvel[ix, iz, 1] < pvel[ix, iz + 1, 1]:
                        pvel[ix, iz, 1] = pvel[ix, iz + 1, 1]
        elif fixmethod == 2:
            for ix in range(pnx - 1):
                for iz in range(pnz - 2, -1, -1):  # from top to bottom
                    # print(ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz])
                    if pdens[ix, iz] < pdens[ix, iz + 1]:
                        print(
                            "Fix (2): ",
                            ix,
                            iz,
                            pmodel.x[ix, iz],
                            pmodel.z[ix, iz],
                            "{:15.5e}".format(pdens[ix, iz]),
                            "{:15.5e}".format(pdens[ix + 1, iz]),
                        )

                        pdens[ix, iz] = pdens[ix + 1, iz]
                        if pg2d is not None:
                            pg2d[ix, iz] = pg2d[ix + 1, iz]

                        if pvel is not None:
                            pvel[ix, iz, 0] = pvel[ix + 1, iz, 0]
                            pvel[ix, iz, 2] = pvel[ix + 1, iz, 2]
                    # check explicitly for vy
                    if (pvel is not None) and pvel[ix, iz, 1] < pvel[ix, iz + 1, 1]:
                        pvel[ix, iz, 1] = pvel[ix + 1, iz, 1]
        elif fixmethod == 3:  # fixes only the vy ... in the disk should never be zero
            for iz in range(pnz - 2):  # from bottom to top
                for ix in range(pnx - 2, -1, -1):  # outside to inside
                    if (
                        pvel is not None
                        and pvel[ix, iz, 1] < pvel[ix + 1, iz, 1]
                        and pvel[ix, iz, 1] <= 0.0
                        and (pmodel.z[ix, iz] / pmodel.x[ix, iz]) < 1.0
                    ):
                        # print("Fix (3): ",ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz],"{:15.5e}".format(pdens[ix,iz]),"{:15.5e}".format(pdens[ix+1,iz]))
                        print(
                            "Fix (3): ",
                            ix,
                            iz,
                            pmodel.x[ix, iz],
                            pmodel.z[ix, iz],
                            pvel[ix, iz, 1],
                            pvel[ix + 1, iz, 1],
                        )
                        # print("Fix (3): ",ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz],"{:15.5e}".format(pvel[ix,iz,1]),"{:15.5e}".format(pvel[ix+1,iz,1]))

                        pvel[ix, iz, 1] = pvel[ix + 1, iz, 1]

                        # does not really work, because the density can drop towards the inner radius
                        # f = interpolate.interp1d(np.log10(pmodel.x[ix+1:,iz]), np.log10(pdens[ix+1:,iz]), fill_value = "extrapolate")
                        # pdens[ix,iz]=10**f(np.log10(pmodel.x[ix,iz]))
                        # if np.isnan(pdens[ix,iz]): pdens[ix,iz]=pdens[ix+1,iz]
                        # pdens[ix,iz]=pdens[ix+1,iz]

                        # if pg2d is not None: pg2d[ix,iz]=pg2d[ix+1,iz]

        return prhoGas, pnHtot, pvel, pg2d, ptdust, ptgas

    def toProDiMo(
        self, pmodel: Data_ProDiMo, outdir: str = ".", imethod: str = "linear", fixmethod: int = 1
    ) -> Data_ProDiMo:
        """
        Interpolates the given density/velocity structure onto the |prodimo| grid and writes
        the input files for ProDimo.

        The new quantities are written into a copy of `pmodel` and returned.

        Parameters
        ----------

        pmodel :
            the prodimopy model onto which the input structure should be interpolated.

        outdir :
            output directory where the |prodimo| input files are written to.

        imethod :
            interpolation method passed to `scipy.interpolate.griddata`.
            For details see :func:`interpol_spherical`.

        fixmethod :
            method used to fix the input structure after interpolation.
            For details see :func:`interpol_spherical`.


        .. todo:

           - make it general (e.g. file names)

        """

        print("Do the interpolation ...")
        prhoGas, pnHtot, pvel, pg2d, ptdust, ptgas = self.interpol_spherical(
            pmodel, imethod=imethod, fixmethod=fixmethod
        )

        newpmodel = deepcopy(pmodel)

        if prhoGas is not None:
            newpmodel.rhog = prhoGas

        if pnHtot is not None:
            newpmodel.nHtot = pnHtot

        if pg2d is not None:
            newpmodel.d2g = 1.0 / pg2d
            if prhoGas is not None:
                newpmodel.rhod = prhoGas / pg2d

        if pvel is not None:
            newpmodel.velocity = pvel / 1.0e5  # in prodimopy it is km/s

        if ptdust is not None:
            newpmodel.td = ptdust

        if ptgas is not None:
            newpmodel.tg = ptgas

        print("Create the files ...")
        self.write_text(prhoGas, pnHtot, pvel, pg2d, ptdust, ptgas, outdir)

        return newpmodel

    def write_text(self, prhoGas, pnHtot, pvel, pg2d, ptdust, ptgas, outdir):
        """
        Write the input files for |prodimo| in text format.
        """

        if prhoGas is not None:
            ofile = os.path.join(outdir, "pluto_rho.dat")
            print(ofile)
            np.savetxt(outdir + "/pluto_rho.dat", prhoGas)

        if pnHtot is not None:
            np.savetxt(outdir + "/pluto_dens.dat", pnHtot)

        if pvel is not None:
            ofile = os.path.join(outdir, "pluto_vx.dat")
            print(ofile)
            np.savetxt(ofile, pvel[:, :, 0])
            ofile = os.path.join(outdir, "pluto_vy.dat")
            print(ofile)
            np.savetxt(ofile, pvel[:, :, 1])
            ofile = os.path.join(outdir, "pluto_vz.dat")
            print(ofile)
            np.savetxt(ofile, pvel[:, :, 2])

        if pg2d is not None:
            ofile = os.path.join(outdir, "pluto_gd.dat")
            print(ofile)
            np.savetxt(ofile, pg2d)

        if ptdust is not None:
            ofile = os.path.join(outdir, "pluto_tdust.dat")
            print(ofile)
            np.savetxt(ofile, ptdust)

        if ptgas is not None:
            ofile = os.path.join(outdir, "pluto_tgas.dat")
            print(ofile)
            np.savetxt(ofile, ptgas)

    def write_fits(self, filename="in2D.fits", comments=None):
        """
        NOT YET IMPLEMENTED!

        Write the 2D data of this object as input for |prodimo| as a fits file.
        Quantities that are `None` will be skipped.

        Parameters
        ----------

        rhoGas : array_like
          the gas density in g/cm3; DIMENSION: (nx,nz)

        nHtot : array_like
          the particle number density in g/cm3; DIMENSION: (nx,nz)

        g2d : array_like
          the gas to dust mass ratio; DIMENSION: (nx,nz)

        velocity : array_like
          disk velocity vector at each position in the disk vx,vy,vz in cm/s; DIMENSION: (nx,nz,3)

        filename : str
          the output filename/path optional.

        comments : don't know yet
          comments added to the fits file

        """

        print("Not yet implemented!")

        return

    def get_pmodel(self) -> Data_ProDiMo:
        """
        Returns the data as a :class:`~prodimopy.read.Data_ProDiMo` object.

        Can be useful for plotting (e.g. use the prodimopy plotting routines)

        Returns
        -------
        pmodel : :class:`~prodimopy.read.Data_ProDiMo`
          the prodimopy representation of this 2D input structure.

        """

        pmodel = Data_ProDiMo(name="input model")

        pmodel.x = self.x / autocm
        pmodel.z = self.z / autocm
        pmodel.nx = pmodel.x.shape[0]
        pmodel.nz = pmodel.x.shape[1]
        if self.rhoGas is None:
            pmodel.nHtot = self.nHtot
        else:
            pmodel.rhog = self.rhoGas

        # Fixme: that does not work if rhoGas is not set
        if self.g2d is not None:
            pmodel.d2g = 1.0 / self.g2d
            # that does not work if we just have nHtot ... so just don't do it
            # pmodel.rhod=self.rhoGas*pmodel.d2g

        pmodel.td = self.tdust
        pmodel.tg = self.tgas

        pmodel.velocity = self.velocity / 1.0e5

        return pmodel
