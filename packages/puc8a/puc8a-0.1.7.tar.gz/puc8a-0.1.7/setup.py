from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except:
    long_description = ''

setup(name='puc8a',
      version='0.1.7',
      description='Assembler and C compiler for the PUC8a processor',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/wcaarls/puc8a',
      author='Wouter Caarls',
      author_email='wouter@puc-rio.br',
      license='GPL-3.0-or-later',
      classifiers=['Development Status :: 4 - Beta',
      'Environment :: Console',
      'Programming Language :: Python :: 3',
      'Topic :: Education',
      'Topic :: Software Development :: Assemblers',
      'Topic :: Software Development :: Compilers',
      ],
      keywords='assembler compiler educational risc processor',
      packages=find_packages(),
      package_data={'': ['*.grammar']},
      entry_points = {
        'console_scripts': ['as-puc8a=puc8a.asm:main',
                            'cc-puc8a=puc8a.cc:main']
      })
