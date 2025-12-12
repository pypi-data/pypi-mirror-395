# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:58:32 2024

@author: lrussell
"""

from distutils.core import setup
from pathlib import Path

setup(
  name = 'w2rpy',    
  py_modules=['w2rpy'],
  version = '0.3.23',     
  license='MIT',        
  description = 'Geospatial and Hydraulic Functions For Analysis of River Systems',   
  author = 'Luke Russell',                   
  author_email = 'lrussell@wolfwaterresources.com',      
  install_requires=['pandas',
                    'openpyxl',
                    'numpy',
                    'shapely',
                    'geopandas',
                    'rasterio',
                    'pysheds',
                    'scipy',
                    'matplotlib'],
  long_description = (Path(r'C:/Users/lrussell/Desktop/WRFpy/w2rpy') / 'README.md').read_text(),
  long_description_content_type='text/markdown'
  )

