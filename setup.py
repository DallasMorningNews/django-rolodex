import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rolodex',
    version='0.1.2.4',
    packages=['rolodex'],
    include_package_data=True,
    license='MIT License',
    description='A Django app for managing relationships between people and organizations.',
    long_description=README,
    url='https://github.com/DallasMorningNews/django-rolodex/',
    author='Jon McClure',
    author_email='jon.r.mcclure@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    install_requires = ['Django>=1.7','djangorestframework>=2.4.4', 'dj-database-url>=0.3.0','networkx>=1.9.1',],
)
