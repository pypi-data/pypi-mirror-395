
import setuptools

with open( "README.md", "r") as filein:
  long_description = filein.read()

setuptools.setup(
  name = 'rskfd',
  #packages = ['rskfd','rskfd.remote_control','rskfd.iq_data_handling','rskfd.signal_generation','rskfd.helper'],
  #packages = setuptools.find_packages(),
  packages = setuptools.find_namespace_packages(),
  version = '0.5.4',
  license='MIT',
  description = 'Python Package for Instrument Control and Data Handling',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'Florian Ramian', 
  author_email = 'gitlab@ramian.eu',
  url = 'https://gitlab.com/ramian/rskfd',   # gitlab
  download_url = 'https://gitlab.com/ramian/rskfd/',
  keywords = ['INSTRUMENT CONTROL', 'I/Q DATA','WV','IQ.TAR'],
  install_requires=[
          'numpy',
          'scipy'
      ],
  python_requires='>=3.0',
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
