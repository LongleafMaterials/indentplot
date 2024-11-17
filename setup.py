from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Indentation plotting utility.'
LONG_DESCRIPTION = 'Utility for plotting hardness data (microhardness, nanoindentation, etc.) overlaid on micrographs or images.'

# Setting up
setup(
        name="indentplot", 
        version=VERSION,
        author="Colin fletcher",
        author_email="<colin@longleafresearch.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
