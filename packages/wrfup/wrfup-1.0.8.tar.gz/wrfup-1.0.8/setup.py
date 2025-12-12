from setuptools import setup, find_packages

setup(
    name='wrfup',
    version='1.0.8',
    description='A Python package to ingest global urban data into WRF geo_em files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jacobogabeiraspenas/wrfup',
    author='Jacobo Gabeiras Penas',
    author_email='jacobogabeiras@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24,<2.0",
        "tqdm>=4.62,<5.0",
        "requests>=2.32,<3.0",
        "netCDF4>=1.7,<2.0",
        "pandas>=2.2,<3.0",
        "shapely>=2.0,<3.0",
        "fiona>=1.10,<2.0",
        "rasterio>=1.4,<2.0",
        "xarray>=2024.7,<2025.0",
        "scipy>=1.13,<2.0"
    ],
    entry_points={
        'console_scripts': [
            'wrfup=wrfup.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

