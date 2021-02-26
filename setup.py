from setuptools import setup, find_packages

setup(name='file_iterator',
    version='0.0.1',
    description='Utilities for iterating file contents.',
    url='https://github.com/ferancona/file-iterator',
    author='Fernando Ancona',
    author_email='',
    install_requires=[
        'events'
    ],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False
)