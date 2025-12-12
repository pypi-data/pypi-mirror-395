from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='isoring',
    version='0.0.2',
    description='A data security structure, IsoRing, and a brute-force environment.',
    long_description=readme,
    author='Richard Pham',
    author_email='phamrichard45@gmail.com',
    url='https://github.com/Changissnz/isoring',
    #license=LICENSE,
    packages=find_packages(exclude=('tests','docs'))
)
