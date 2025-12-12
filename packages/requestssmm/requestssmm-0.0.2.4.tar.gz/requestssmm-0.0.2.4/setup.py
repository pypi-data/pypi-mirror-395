from setuptools import setup, find_packages

setup(
    name='requestssmm',
    version='0.0.2.4',
    packages=find_packages(include=['requestssmm', 'requestssmm.*']),
    install_requires=[
        'requests',
        'fb_atm',
        'mahdix'
    ],
    include_package_data=True,
)

"""
pypi-AgEIcHlwaS5vcmcCJGVlNGJhZGM2LTA1ZDItNGMxYS04MWQzLTI4ZDAwNWQxYWI5ZAACKlszLCIyNmY0NzMzMS01OTEzLTRiODQtODQ4MS0zNmU4YzFmNDFjMzciXQAABiBM61PeNHd-rgBN4gaLpt43W7l_eRXM1scFUO6pve5K5g
"""




