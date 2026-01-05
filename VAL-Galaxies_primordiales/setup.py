"""Setup script for VAL-Galaxies_primordiales package"""

from setuptools import setup, find_packages

setup(
    name='val-galaxies-primordiales',
    version='0.1.0',
    description='Validation du modèle JANUS par confrontation aux galaxies primordiales',
    author='JANUS Collaboration',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    install_requires=[
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'matplotlib>=3.7.0',
        'astropy>=5.3.0',
        'emcee>=3.1.0',
        'corner>=2.2.0',
    ],
    extras_require={
        'dev': ['pytest>=7.4.0', 'pytest-cov>=4.1.0'],
    },
)
