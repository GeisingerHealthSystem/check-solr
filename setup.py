"""
A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

#
# Python setup file for hdp_tools library
#

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
	name='check-solr',
	version='0.0.1',
	description='Various tools and functions for the Hadoop operations team.',
	url='https://github.com/GeisingerHealthSystem/python-udaopstools',
	author='Daniel Martin',
	author_email='djmartin6@geisinger.edu',
	license='No license',
	python_requires='>=3.0.0',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Programming Language :: Python :: 3.8',
	],
	keywords='sys-decom decom allscripts solr',
	packages=['checksolr'],
	# Do NOT add urllib3 here, it will be pulled in as part of requests
	# This is due to urllib3 and requests not always being in sync
	# Refernce https://github.com/kennethreitz/requests/blob/master/setup.py
	# Note also that thift here is fine, but our modified python-apache-thrift
	#	is used as an RPM that mimics this outside virtual envs with a different
	#	naming
	install_requires=[
	],
    entry_points={
        'console_scripts': ['check-solr = checksolr.__main__:main']
    },
	zip_safe=False
)

