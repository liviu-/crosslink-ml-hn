import os
from setuptools import setup, find_packages

package_name = 'crosslinking_bot'
version_file = 'version.py'

def get_version(package_name=package_name, filename=version_file):
    """Retrieve version from package_name/filename

    Assumes that version is the only line in the file,
    and it's a module-level declaration following 
    the format of `__version__ = 'x.y.z'`
    """
    version_path = os.path.join(package_name, version_file)
    return open(version_path).read().split('=')[-1].strip(' \'"\n')

setup(
    name='hn_crosslinking_bot',
    url='https://github.com/liviu-/crosslink-ml-hn',
    version=get_version(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'crosslinking_bot = crosslinking_bot.crosslinking_bot:run_bot'
        ]
    },
    install_requires=[
        'praw',
        'requests',
        'ptest',
        'urltools'
    ],
    license='MIT',
    long_description=open('README.md').read(),
)
