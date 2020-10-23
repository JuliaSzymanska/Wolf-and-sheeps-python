from distutils.core import setup

import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name='chase',
    version='1.3',
    # todo
    description='TODO',
    author='Przemysław Zdrzalik, Julia Szymańska',
    author_email='224466@edu.p.lodz.pl, 224411@edu.p.lodz.pl',
    packages=['chase'],
)
