from setuptools import setup, find_packages
from codecs import open
from os import path
from prime_minister.version import VERSION

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='bpss_prime_minister',
    version=VERSION,
    description='Demo flask web app listing prime ministers of Australia',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timcu/bpss-prime-minister',
    author="D Tim Cummings",
    author_email='tim@triptera.com.au',  # Optional
    license='MIT',
    classifiers=[ 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='flask bpss pm',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3',
    install_requires=['flask_bootstrap', 'python-dotenv'],
    include_package_data=True,
)
