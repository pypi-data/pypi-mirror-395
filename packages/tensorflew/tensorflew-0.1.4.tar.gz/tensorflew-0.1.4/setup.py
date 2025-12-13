import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tensorflew',
    version='0.1.4',  # Increment this version number from your previous release
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for time series forecasting techniques',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tensorflew',  # Update with your repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'statsmodels',
        'scikit-learn',
    ],
)
