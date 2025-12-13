"""A setuptools based setup module.
"""

from codecs import open
from os import path

from setuptools import find_namespace_packages, setup

# To use a consistent encoding
here=path.abspath(path.dirname(__file__))
  
# Get the long description from the relevant file
with open(path.join(here,'DESCRIPTION.md'),encoding='utf-8') as f:
    long_description=f.read()


setup(
    name='prodimopy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    #version="5.0", 

    description='Python tools for ProDiMo and slab models',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://gitlab.astro.rug.nl/prodimo/prodimopy/',

    project_urls={
        'Changelog': 'https://prodimopy.readthedocs.io/en/stable/changelog.html',
        'Bug Reports': 'https://gitlab.astro.rug.nl/prodimo/prodimopy/-/issues',
        'Documentation': 'https://prodimopy.readthedocs.io/en/stable/'
    },

    # Author details
    author='Christian Rab',
    author_email='rab@mpe.mpg.de',

    # Choose your license
    license='MIT License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.10',
    ],

    # What does your project relate to?
    keywords='astronomy astrophysics star-formation protoplanetary-disks modelling',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_namespace_packages(),

    include_package_data=True,
    package_data={'prodimopy/stylelib': ['prodimopy/stylelib/prodimopy.mplstyle','prodimopy/stylelib/prodimopy_nb.mplstyle']},

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
                      'astropy>=5.1',
                      'matplotlib>=3.7',
                      'numpy>=1.20',  # no special requirements, but astropy has some
                      'scipy>=1.7.1',
                      'f90nml>=1.4.4', # for reading the Parameters namelist
                      'pandas>=1.5',  # the last three are only for slab models.
                      'adjustText>=0.8',  # just to avoid the beta version
                      'spectres>=2.2.0',
                      'dust_extinction>=1.5',
                      'typing_extensions>4.12.0',
                      'tqdm>=4.67'
                      ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #    'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
      'console_scripts': [
        'pplot=prodimopy.script_plot:main',
        'pplot_models=prodimopy.script_plot_models:main',
        'pcompare=prodimopy.script_compare:main',
        'pparam=prodimopy.script_params:main',
        'pcpforrestart=prodimopy.script_cpforrestart:main',
        'prunprodimo=prodimopy.script_runprodimo:main',
         ],
    },
)
