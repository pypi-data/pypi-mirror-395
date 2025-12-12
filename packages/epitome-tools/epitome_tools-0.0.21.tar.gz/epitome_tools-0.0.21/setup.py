#this is a setup.py file
from setuptools import setup, find_packages

VERSION = '0.0.21'
DESCRIPTION = 'Auxiliary tools for the Consensus Pituitary Atlas'
LONG_DESCRIPTION = 'Python package containing auxiliary tools for the Consensus Pituitary Atlas. The current workflow commands allow celltyping and doublet detection with a single line of code, for more information see https://github.com/BKover99/epitome_tools'


setup(
    name="epitome_tools",
    version=VERSION,
    author="Bence Kover",
    author_email="<kover.bence@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
package_data={
        'epitome_tools': ['models/*'],
    },
    install_requires=[
	'xgboost',
	'scipy',
	'numpy'
	],
include_package_data=True,
    keywords=['xgboost', 'annotation', 'celltype', 'doublet'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ]
)

