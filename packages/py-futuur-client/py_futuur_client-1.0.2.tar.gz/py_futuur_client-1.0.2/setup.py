from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='py-futuur-client', 
    version='1.0.2',
    packages=find_packages(),
    
    author='Futuur .inc',
    author_email='support@futuur.com',
    description='A client to interact with Futuur public API.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/futuur/py_futuur_client.git',
    license='MIT',
    
    install_requires=[
        'requests>=2.32.5', 
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='futuur api client trading prediction-market',
)