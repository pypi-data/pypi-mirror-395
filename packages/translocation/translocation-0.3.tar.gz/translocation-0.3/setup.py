from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='translocation',
    version='0.3',
    description="Correction of translocation defects in crystals",
    long_description=long_description,
    author="Petr Kolenko",
    author_email='kolenpe1@cvut.cz',
    url='https://github.com/kolenpe1/translocation',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
#    entry_points={
#        'console_scripts': [
#            'translocation = translocation.source:main',
#        ],
#    },
    zip_safe=False,
)
