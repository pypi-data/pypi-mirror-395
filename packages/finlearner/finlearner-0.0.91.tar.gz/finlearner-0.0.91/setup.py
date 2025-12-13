from setuptools import setup, find_packages

# Package metadata
NAME = 'finlearner'
DESCRIPTION = 'A professional-grade financial analysis library featuring Deep Learning (LSTM, PINNs), Portfolio Optimization, and Advanced Technical Analysis. It is the final beta upgrade of finlearn.'
VERSION = '0.0.91'  # Bumped version for major upgrade
AUTHOR = 'Ankit Dutta'
AUTHOR_EMAIL = 'ankitduttaiitkgp@gmail.com'
URL = 'https://github.com/ankitdutta428/finlearn'
LICENSE = 'Apache 2.0'

# Read long description from README file
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Define dependencies
INSTALL_REQUIRES = [
    'numpy',
    'pandas',
    'yfinance',
    'plotly',
    'matplotlib',
    'seaborn',
    'scipy',          # For Black-Scholes math
    'scikit-learn',   # For preprocessing/scaling
    'tensorflow',     # For PINNs and LSTMs
]

# specialized dependencies for development/testing
EXTRAS_REQUIRE = {
    'dev': ['pytest', 'twine', 'wheel'],
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    
    # Correctly map the src directory
    packages=find_packages(),
    
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>=3.8',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)