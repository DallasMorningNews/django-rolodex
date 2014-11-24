import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rolodex',
    version='0.1.0.dev1',
    packages=['rolodex'],
    include_package_data=True,
    license='MIT License',
    description='A Django app for managing relationships between people and organizations.',
    long_description=README,
    url='http://www.example.com/',
    author='Jon McClure',
    author_email='jon.r.mcclure@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = ['Django>=1.7','djangorestframework>=2.4.4',],
)
