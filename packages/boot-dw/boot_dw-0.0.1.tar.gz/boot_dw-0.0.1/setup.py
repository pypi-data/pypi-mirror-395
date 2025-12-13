"""
Setup script for boot_dw package.
"""

from setuptools import setup, find_packages
import os

# Read long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='boot_dw',
    version='0.0.1',
    author='Dr. Merwan Roudane',
    author_email='merwanroudane920@gmail.com',
    description='Bootstrap tests for autocorrelation in regression models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/merwanroudane/bootdw',
    project_urls={
        'Bug Reports': 'https://github.com/merwanroudane/bootdw/issues',
        'Source': 'https://github.com/merwanroudane/bootdw',
        'Documentation': 'https://github.com/merwanroudane/bootdw#readme',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='econometrics statistics autocorrelation durbin-watson bootstrap time-series regression',
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.20.0',
        'scipy>=1.7.0',
    ],
    extras_require={
        'dev': ['pytest>=6.0', 'pytest-cov>=2.0', 'flake8>=3.9'],
        'docs': ['sphinx>=4.0', 'sphinx-rtd-theme>=0.5'],
    },
    include_package_data=True,
    zip_safe=False,
)
