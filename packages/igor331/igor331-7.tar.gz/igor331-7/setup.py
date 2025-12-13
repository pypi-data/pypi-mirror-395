from setuptools import setup, find_packages

VERSION = '7' 
DESCRIPTION = 'package generale per Pyhton'
LONG_DESCRIPTION = 'descrizione lunga del primo package'

# Impostazioni
setup(
       # il nome deve essere uguale a quello della cartella 'verysimplemodule'
        name="igor331", 
        version=VERSION,
        author="Igor Bonat",
        author_email="<igorbonat@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas','numpy'], # aggiungi qualsiasi package addizionale che 
        # deve essere installato insieme al tuo package. Ad Es. 'caer'
        
        keywords=['python', 'esempio package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)