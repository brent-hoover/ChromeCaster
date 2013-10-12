import os
import io
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
import chromecaster


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='ChromeCaster',
    version=chromecaster.__version__,
    packages=['chromecaster'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask>=0.10.1', 'walkdir==0.3'],
    url='https://github.com/zenweasel/ChromeCaster',
    license='Apache',
    author='Brent Hoover',
    author_email='brent@hoover.net',
    long_description=read('README.rst'),
    platforms='any',
    description='A Simple local webserver for serving video and audio files to view them on ChromeCast',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
