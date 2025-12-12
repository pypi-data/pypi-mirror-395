#!/bin/bash

# All credit for this script goes to Andy Morris (@anmorris),
# who wrote this script for the LHCb Starterkit documentation.

#check you have access to pip
if [[ "$(which pip)" == "" ]]
then
	echo "ERROR: to build the docs you must have access to 'pip'!"
	exit 1
fi

#check if a connection to pip is available (i.e. an internet connection)
if wget -q --spider https://pypi.org/project/pip/
then

	#verions
	MKDOCS_VERSION=$(grep "mkdocs==" environment-docs.yml | cut -d= -f3)
	MATERIAL_VERSION=$(grep "mkdocs-material==" environment-docs.yml | cut -d= -f3)
    DOCSTRINGS_VERSION=$(grep "mkdocstrings-python==" environment-docs.yml | cut -d= -f3)
	JUPYTER_VERSION=$(grep "mkdocs-jupyter==" environment-docs.yml | cut -d= -f3)

	#update needed packages
	pip install --upgrade pip setuptools wheel
	pip install mkdocs==${MKDOCS_VERSION} mkdocs-material==${MATERIAL_VERSION} mkdocstrings-python==${DOCSTRINGS_VERSION} mkdocs-jupyter==${JUPYTER_VERSION}
	# if [[ -f requirements.txt ]]; then pip install -r requirements.txt; fi;

else
	echo "WARNING: Could not connect to pypi.org, will continue hoping that the packages are installed and up to date..."
	echo "       : N.B. the LaTeX compiler requires internet access, without a connection it may not render correctly..."
fi

#build!
python -m mkdocs build -d public

if [[ -f _redirects ]]; then cp _redirects public; fi;
