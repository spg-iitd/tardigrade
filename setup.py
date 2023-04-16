from setuptools import setup

classifiers = []

setup(
    name='tardigrade',
    version='0.0.1',
    description='A library for collection of IDS & robust-IDS and tools for evaluating them',
    long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='https://github.com/spg-iitd/tardigrade',
    author='Swain Subrat Kumar',
    author_email='mailofswainsubrat@gmail.com',
    license='MIT',
    # classifiers=classifiers,
    keywords='ids adversarial network nids',
    packages=['tardigrade'],
    install_requires=[''],
    zip_safe=False
)
