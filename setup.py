import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
setup(
    name='ChromeCaster',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'walkdir'],
    url='https://github.com/zenweasel/ChromeCaster',
    license='MIT',
    author='Brent Hoover',
    author_email='brent@hoover.net',
    description='A Simple local webserver for serving video and audio files to view them on ChromeCast'
)
