#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='OpenFisca-Mali',
    version='1.1.6',
    author='OpenFisca Team',
    author_email='contact@openfisca.fr',
    description=u'OpenFisca tax and benefit system for Mali',
    keywords='benefit microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/openfisca/openfisca-mali',
    include_package_data=True,  # Will read MANIFEST.in
    install_requires=[
        'OpenFisca-Core >=34.2.2,<35.0',
        ],
    extras_require = {
        'dev': [
            "autopep8 ==1.4.4",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            "pytest <6.0",
            "scipy >= 0.17",  # Only used to test de_net_a_brut reform
            "requests >= 2.8",
            "openfisca-ceq >=0.2.6",
            "openfisca-survey-manager[dev] >= 0.34, <1.0",
            "yamllint >=1.11.1,<1.19",
            ],
        'ceq': [
            "openfisca-ceq >=0.2.6",
            ],
        },
    packages=find_packages(),
    )
