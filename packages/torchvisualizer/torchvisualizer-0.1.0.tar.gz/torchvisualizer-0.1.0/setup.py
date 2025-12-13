# setup.py
from setuptools import setup, find_packages

setup(
    name='torchvisualizer',
    version='0.1.0',
    description='A utility for visualizing PyTorch model architectures.',
    long_description=open('README.md',encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='Vidit Gupta',
    packages=find_packages(), # Automatically finds the 'arch_plotter' directory
    install_requires=[
        'torch>=1.10.0',
        'matplotlib>=3.5.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)