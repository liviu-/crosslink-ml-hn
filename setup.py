from setuptools import setup, find_packages

setup(
    name='hn_crosslinking_bot',
    version='0.1dev',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'crosslinking_bot = crosslinking_bot.__main__:main'
        ]
    },
    install_requires=[
        'praw',
        'requests',
        'ptest',
        'urltools'
    ],
    license='MIT',
    url='https://github.com/liviu-/crosslink-ml-hn',
    long_description=open('README.md').read(),
)
