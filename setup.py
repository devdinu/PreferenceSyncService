from setuptools import setup

setup(name='PrefSyncService',
      version='1.0',
      description='PrefSync Service For syncing Sublime Text User Packages',
      author='Dinesh Kumar',
      author_email='dineshkumar_cse@hotmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[ 'bottle', 'pymongo'],
)
