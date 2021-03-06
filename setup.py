from setuptools import setup, find_packages

setup (
    name='file-iterator',
    packages=find_packages(),
    version='1.0.0',
    license='MIT',
    description='Utilities for iterating file contents.',
    author='Fernando Ancona',
    author_email='f.anconac@gmail.com',
    url='https://github.com/ferancona/file-iterator',
    download_url = '',
    keywords = ['FILE', 'READ', 'CONTENT', 'ITERATION'],
    install_requires=[
        'events'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
    python_requires='>=3.5',
    zip_safe=False
)